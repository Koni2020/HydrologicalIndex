from pathlib import Path
import sys
import pandas as pd

# Allow importing hydrological_index.py from the repository root
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from hydrological_index import main_compute

input_file = REPO_ROOT / "examples" / "example_input.csv"
output_dir = REPO_ROOT / "outputs"
output_dir.mkdir(exist_ok=True)

sf = pd.read_csv(input_file, index_col=0, parse_dates=True)

signatures = main_compute(sf)

output_file = output_dir / "annual_streamflow_signatures_example.csv"
signatures.to_csv(output_file)

print(f"Annual streamflow signatures saved to: {output_file}")
