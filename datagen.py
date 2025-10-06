#!/usr/bin/env python3
# pii_data_generator.py
#
# Generate synthetic PII CSVs for testing the HMAC join + incremental pipeline.
#
# Example:
#   python pii_data_generator.py --master /tmp/master.csv --new /tmp/new.csv --count-master 1000 --overlap 0.6
#
# Output:
#   - master.csv (initial dataset)
#   - new.csv (contains overlapping + new records)

import csv, random, argparse
from datetime import datetime, timedelta
from faker import Faker

def parse_args():
    p = argparse.ArgumentParser(description="Generate fake PII CSVs for incremental match testing")
    p.add_argument("--master", required=True, help="Path to master CSV output")
    p.add_argument("--new", required=True, help="Path to new CSV output")
    p.add_argument("--count-master", type=int, default=1000, help="Number of master records (default 1000)")
    p.add_argument("--overlap", type=float, default=0.5, help="Fraction of master records reused in new batch (0–1)")
    p.add_argument("--count-new", type=int, default=None, help="Number of new-batch records (default = count-master)")
    return p.parse_args()

def make_fake_person(fake: Faker, idx: int):
    # generate random date of birth between 1970 and 2005
    dob = fake.date_of_birth(minimum_age=20, maximum_age=55)
    phone = fake.msisdn()[:10]
    email = fake.email()
    return {
        "id": idx,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": email,
        "dob": dob.strftime("%Y-%m-%d"),
        "phone": phone,
        "city": fake.city(),
        "country": fake.country()
    }

def main():
    args = parse_args()
    fake = Faker()
    Faker.seed(42)
    random.seed(42)

    master_count = args.count_master
    new_count = args.count_new or args.count_master
    overlap_fraction = max(0.0, min(1.0, args.overlap))

    master_records = [make_fake_person(fake, i + 1) for i in range(master_count)]

    # Choose subset for overlap
    overlap_count = int(new_count * overlap_fraction)
    overlap_records = random.sample(master_records, min(overlap_count, len(master_records)))

    # Generate fresh new records
    fresh_count = new_count - len(overlap_records)
    fresh_records = [make_fake_person(fake, 100000 + i + 1) for i in range(fresh_count)]

    new_records = overlap_records + fresh_records
    random.shuffle(new_records)

    # write CSVs
    fieldnames = list(master_records[0].keys())
    for path, rows in [(args.master, master_records), (args.new, new_records)]:
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(rows)
        print(f"✓ Wrote {len(rows):,} records to {path}")

if __name__ == "__main__":
    main()
