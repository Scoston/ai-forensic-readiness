#!/usr/bin/env python3
"""Run the two conditions of one local simulation and write a reviewable result."""
import argparse
from pathlib import Path

from evidence import write_json
from simulations import standalone


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", type=int, choices=range(1, 11), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output already exists; choose a new path to preserve the prior result")
    write_json(args.output, standalone(args.case))
    print(f"Wrote both simulated conditions to {args.output}")


if __name__ == "__main__":
    main()
