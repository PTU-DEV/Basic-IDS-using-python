from pathlib import Path
import pandas as pd

project_root = Path(__file__).resolve().parents[1]
input_file = project_root / "dataset" / "KDDTest.arff"
output_file = project_root / "dataset" / "KDDTest.csv"

columns = []
data_started = False
data_rows = []

with open(input_file, "r", errors="ignore") as f:
    for line in f:
        line = line.strip()
        
        # Read attributes
        if line.lower().startswith("@attribute"):
            parts = line.split()
            col_name = parts[1].replace("'", "").replace('"', "")
            columns.append(col_name)
        
        # Detect start of data
        elif line.lower().startswith("@data"):
            data_started = True

        # Read data rows
        elif data_started and line and not line.startswith("%"):
            row = [x.strip() for x in line.split(",")]
            data_rows.append(row)

# Create DataFrame
df = pd.DataFrame(data_rows, columns=columns)
df.to_csv(output_file, index=False)

print("Converted successfully →", output_file)
print(df.head())
print("Columns:", len(columns))
print("Rows:", len(df))
