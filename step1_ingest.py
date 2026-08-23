import os
import pandas as pd

def ingest_dataset(filepath: str) -> pd.DataFrame:
    """Step 1: Ingests raw data (CSV/XLSX), auto-detects delimiter, and removes duplicates."""
    print("📥 Step 1: Ingesting dataset & de-duplicating...")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Input file not found: {filepath}")

    if filepath.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(filepath, dtype=str)
    else:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            first_line = f.readline()
            sep = '|' if '|' in first_line else ('\t' if '\t' in first_line else ',')
        df = pd.read_csv(filepath, sep=sep, skipinitialspace=True, dtype=str)

    df.columns = df.columns.str.strip()
    df = df.dropna(how='all', axis=1)

    initial_count = len(df)
    subset = [c for c in ['Mfg_Part_Num', 'Part_Desc'] if c in df.columns]
    if subset:
        df = df.drop_duplicates(subset=subset, keep='first')

    print(f"   ✅ Ingested {len(df)} items ({initial_count - len(df)} duplicates removed)")
    return df