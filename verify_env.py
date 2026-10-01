"""
Pre-flight environment check. Run this BEFORE pulling the model or training.

Confirms every package imports, prints versions, and — the point for your
A100 — reports whether torch sees CUDA and whether the GPU supports bf16,
so you know `bf16=True` will actually take before you start a training run.

Usage:
    python verify_env.py
"""

import importlib
import sys

# (import name, pip name) — import name differs from pip name for sklearn
PACKAGES = [
    ("torch", "torch"),
    ("transformers", "transformers"),
    ("tokenizers", "tokenizers"),
    ("sentencepiece", "sentencepiece"),   # DeBERTa-v3 tokenizer dies without this
    ("google.protobuf", "protobuf"),
    ("datasets", "datasets"),
    ("sklearn", "scikit-learn"),
    ("pandas", "pandas"),
    ("numpy", "numpy"),
    ("accelerate", "accelerate"),         # Trainer dies without this
]


def check_imports() -> bool:
    print(f"Python: {sys.version.split()[0]}\n")
    ok = True
    for import_name, pip_name in PACKAGES:
        try:
            mod = importlib.import_module(import_name)
            ver = getattr(mod, "__version__", "?")
            print(f"  ok   {pip_name:<14} {ver}")
        except ImportError as e:
            ok = False
            print(f"  MISS {pip_name:<14} -> pip install {pip_name}   ({e})")
    return ok


def check_cuda() -> None:
    import torch

    print("\n--- torch / CUDA ---")
    print(f"  torch version        : {torch.__version__}")
    cuda = torch.cuda.is_available()
    print(f"  cuda available       : {cuda}")

    if not cuda:
        print("  -> No GPU visible. Training will run on CPU in fp32 (slow for DeBERTa).")
        print("     If you expected a GPU: check the CUDA torch build + drivers.")
        return

    print(f"  cuda version (torch) : {torch.version.cuda}")
    print(f"  device count         : {torch.cuda.device_count()}")
    for i in range(torch.cuda.device_count()):
        name = torch.cuda.get_device_name(i)
        total = torch.cuda.get_device_properties(i).total_memory / 1e9
        print(f"    [{i}] {name}  ({total:.0f} GB)")

    bf16 = torch.cuda.is_bf16_supported()
    print(f"  bf16 supported       : {bf16}")
    if bf16:
        print("  -> precision_type() will select bf16=True. Good for A100/L4/H100.")
    else:
        print("  -> No bf16; precision_type() will fall back to fp16=True.")


def smoke_test_model() -> None:
    """Optional: load the base model + tokenizer to prove the SentencePiece
    tokenizer and model weights load cleanly. Comment out to skip the download."""
    print("\n--- model smoke test (downloads ~500MB first run) ---")
    try:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification

        mid = "deepset/deberta-v3-base-injection"
        tok = AutoTokenizer.from_pretrained(mid)
        model = AutoModelForSequenceClassification.from_pretrained(mid)
        print(f"  ok   loaded {mid}")
        print(f"  id2label: {model.config.id2label}")
        enc = tok("test input", return_tensors="pt")
        print(f"  ok   tokenizer produced {enc['input_ids'].shape[1]} tokens")
    except Exception as e:
        print(f"  FAIL model/tokenizer load: {e}")
        print("     Most common cause: missing sentencepiece/protobuf.")


if __name__ == "__main__":
    all_ok = check_imports()
    if all_ok:
        check_cuda()
        smoke_test_model()
        print("\nEnvironment looks good." if all_ok else "")
    else:
        print("\nSome packages missing — install them (pip install -r requirements.txt) and re-run.")
        sys.exit(1)
