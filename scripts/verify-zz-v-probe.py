#!/usr/bin/env python3
# ci-line: B3 | V probe (throwaway: a new verifier joins B3 by its header alone) | --hello
"""Throwaway (contract V proof): a PR that adds only this file must run it in group B3. Deleted after."""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
page = os.path.join(ROOT, "games/split-it/index.html")
print("V probe ran with", sys.argv[1:], "; split-it page present:", os.path.exists(page))
sys.exit(0 if os.path.exists(page) else 1)
