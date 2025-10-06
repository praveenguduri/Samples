#!/usr/bin/env python3
# pii_incremental_join.py
#
# Incremental matching:
#   - Read MASTER CSV (may already have join_key, bucket_id)
#   - Read NEW CSV (raw PII)
#   - Build HMAC join_key + bucket_id for NEW (and MASTER if missing)
#   - Join on (bucket_id, join_key) to get matches
#   - Optionally write new_only and updated_master
#
# Example:
#   export HMAC_SECRET="super-secret-local-only"
#   spark-submit pii_incremental_join.py \
#     --master /path/to/master.csv \
#     --new /path/to/new.csv \
#     --out-matches /path/to/out/matches \
#     --pii-spec '[{"col":"email","type":"email"},{"col":"dob","type":"date"},{"col":"phone","type":"phone"}]' \
#     --num-buckets 200 \
#     --out-new-only /path/to/out/new_only \
#     --out-updated-master /path/to/out/updated_master

import os, re, json, argparse, hmac, hashlib
from typing import Optional, List, Dict
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql import types as T

def parse_args():
    p = argparse.ArgumentParser("Incremental HMAC join (CSV->CSV)")
    p.add_argument("--master", required=True, help="Existing MASTER CSV (may contain join_key, bucket_id)")
    p.add_argument("--new", required=True, help="NEW batch CSV (raw PII)")
    p.add_argument("--out-matches", required=True, help="Output folder for matched records CSV")
    p.add_argument("--out-new-only", default=None, help="(Optional) Output folder for records only in NEW")
    p.add_argument("--out-updated-master", default=None, help="(Optional) Output folder for MASTER ∪ new_only")
    p.add_argument("--pii-spec", required=True,
                   help="JSON array in canonical order, e.g. "
                        "'[{\"col\":\"email\",\"type\":\"email\"},{\"col\":\"dob\",\"type\":\"date\"}]'")
    p.add_argument("--num-buckets", type=int, default=200, help="Number of buckets (default 200)")
    p.add_argument("--delimiter", default="|", help="Canonical delimiter (default '|')")
    p.add_argument("--secret-env", default="HMAC_SECRET", help="Env var for HMAC key (default HMAC_SECRET)")
    p.add_argument("--repartition", action="store_true", help="Repartition by bucket_id before join/writes")
    return p.parse_args()

def load_secret_bytes(env_name: str) -> bytes:
    v = os.environ.get(env_name)
    if not v:
        raise RuntimeError(f"Env var {env_name} not set")
    return v.encode("utf-8")

def spark_expr_for_normalizer(colname: str, ntype: str):
    c = F.col(colname)
    if ntype == "email":
        return F.lower(F.trim(c))
    if ntype == "phone":
        return F.regexp_replace(c, r"\D+", "")
    if ntype == "date":
        return F.date_format(F.to_date(c), "yyyy-MM-dd")
    if ntype == "lower_trim":
        return F.lower(F.trim(c))
    if ntype == "digits":
        return F.regexp_replace(c, r"\D+", "")
    if ntype == "passthrough":
        return c
    raise ValueError(f"Unknown normalizer type: {ntype}")

def build_hmac_udf(secret_key: bytes):
    @F.udf(T.StringType())
    def hmac_hex(canon: Optional[str]) -> Optional[str]:
        if canon is None:
            return None
        return hmac.new(secret_key, canon.encode("utf-8"), hashlib.sha256).hexdigest()
    return hmac_hex

def add_keys(df, pii_spec: List[Dict[str, str]], secret: bytes, delimiter: str, num_buckets: int):
    norm_cols = [spark_expr_for_normalizer(x["col"], x["type"]) for x in pii_spec]
    canon = F.concat_ws(delimiter, *norm_cols)
    hmac_udf = build_hmac_udf(secret)
    return (df
        .withColumn("join_key", hmac_udf(canon))
        .withColumn("bucket_id",
            (F.xxhash64(F.col("join_key")) % F.lit(num_buckets) + F.lit(num_buckets)) % F.lit(num_buckets)
        )
    )

def ensure_keys(df, pii_spec, secret, delimiter, num_buckets):
    cols = set(df.columns)
    if {"join_key", "bucket_id"}.issubset(cols):
        return df
    # compute if missing
    return add_keys(df, pii_spec, secret, delimiter, num_buckets)

def main():
    args = parse_args()
    secret = load_secret_bytes(args.secret_env)

    spark = SparkSession.builder.appName("PII-Incremental-HMAC-Join").getOrCreate()

    # Read CSVs (header true)
    master = spark.read.option("header", "true").csv(args.master)
    new = spark.read.option("header", "true").csv(args.new)

    # Parse PII spec
    try:
        pii_spec: List[Dict[str, str]] = json.loads(args.pii_spec)
        if not isinstance(pii_spec, list) or not all("col" in x and "type" in x for x in pii_spec):
            raise ValueError
    except Exception as e:
        raise RuntimeError("--pii-spec must be JSON array of {col, type}") from e

    # Ensure both dataframes have join_key + bucket_id
    master_keyed = ensure_keys(master, pii_spec, secret, args.delimiter, args.num_buckets)
    new_keyed = add_keys(new, pii_spec, secret, args.delimiter, args.num_buckets)

    if args.repartition:
        master_keyed = master_keyed.repartition(args.num_buckets, "bucket_id")
        new_keyed = new_keyed.repartition(args.num_buckets, "bucket_id")

    # Matches (inner join on bucket_id + join_key)
    matches = (master_keyed.alias("m")
        .join(new_keyed.alias("n"), on=["bucket_id", "join_key"], how="inner"))

    (matches
        .write.mode("overwrite")
        .option("header", "true")
        .csv(args.out-matches))

    # Optional: only in NEW (left-anti vs MASTER)
    if args.out_new_only:
        new_only = new_keyed.join(master_keyed.select("bucket_id", "join_key").distinct(),
                                  on=["bucket_id","join_key"], how="left_anti")
        (new_only
            .write.mode("overwrite")
            .option("header", "true")
            .csv(args.out_new_only))

    # Optional: updated MASTER = MASTER ∪ NEW_ONLY
    if args.out_updated_master:
        if args.out_new_only:
            new_only_df = new_only
        else:
            new_only_df = new_keyed.join(master_keyed.select("bucket_id", "join_key").distinct(),
                                         on=["bucket_id","join_key"], how="left_anti")
        updated_master = master_keyed.unionByName(new_only_df, allowMissingColumns=True)
        (updated_master
            .write.mode("overwrite")
            .option("header", "true")
            .csv(args.out_updated_master))

    spark.stop()

if __name__ == "__main__":
    main()
