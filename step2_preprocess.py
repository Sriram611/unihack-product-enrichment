import re
import pandas as pd

PLACEHOLDERS = [
    '-- Unbranded --', '-- No Unilog Brand --', '-- No DIB Brand --',
    '-- UNBRANDED --', 'COMMODITY - UNBRANDED', '--', 'None', 'nan', 'NULL', '-'
]

def clean_text(val):
    if pd.isna(val):
        return ''
    s = str(val).strip()
    return '' if s in PLACEHOLDERS else s

def clean_manufacturer(m):
    """Remove distributor codes like Freud Inc (2435) -> Freud Inc"""
    if pd.isna(m):
        return ''
    s = str(m).strip()
    if s in PLACEHOLDERS:
        return ''
    return re.sub(r'\s*\([A-Z0-9_-]+\)', '', s).strip()

def run_step2(df: pd.DataFrame) -> pd.DataFrame:
    """Step 2: Preprocesses raw input data and strips placeholders."""
    df = df.copy()
    df.columns = df.columns.str.strip()

    for col in ['E1_Brand', 'Unilog_Brand', 'DIB_Brand', 'Part_Manuf', 'Mfg_Part_Num', 'Part_Desc']:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)

    if 'Part_Manuf' in df.columns:
        df['Clean_Manuf'] = df['Part_Manuf'].apply(clean_manufacturer)
    else:
        df['Clean_Manuf'] = ''

    return df