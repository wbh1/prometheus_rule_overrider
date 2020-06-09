#! /usr/bin/env python3
from argparse import ArgumentParser
from app.overrider import Overrider

parser = ArgumentParser()
parser.add_argument("dir", help="Directory containing .yml files with overrides")
parser.add_argument(
    "--dest",
    help="Destination to write out the file containing recording rules",
    default="./overrides.rules",
)
parser.add_argument(
    "--stdout", help="Write YAML to STDOUT instead of a file", action="store_true"
)
args = parser.parse_args()

overrider = Overrider(args.dir)
overrider.process()

if not args.stdout:
    with open(f"{args.dest}", "w") as f:
        overrider.dump(f)
else:
    import sys
    overrider.dump(sys.stdout)
