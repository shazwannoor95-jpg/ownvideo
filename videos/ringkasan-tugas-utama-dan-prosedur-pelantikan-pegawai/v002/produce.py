"""Version-specific Full HD pipeline; Google AI Studio Ludo input only."""
import argparse
from production import prepare,assemble
p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--prepare',action='store_true');g.add_argument('--assemble',action='store_true');a=p.parse_args()
if a.prepare:prepare()
else:assemble()
