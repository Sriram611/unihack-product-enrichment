import re

def normalize_uom(val: str, uom: str) -> tuple:
    """Step 7: Standardizes UOM symbols and executes decimal-to-fraction conversions."""
    val_str = str(val).strip().replace('""', '"').replace("''", "'")
    
    # Decimal fraction conversions
    val_str = re.sub(r'(\d+)\.25\b', r'\1-1/4', val_str)
    val_str = re.sub(r'(\d+)\.5\b', r'\1-1/2', val_str)
    val_str = re.sub(r'(\d+)\.75\b', r'\1-3/4', val_str)
    val_str = re.sub(r'(\d+)\.125\b', r'\1-1/8', val_str)
    val_str = re.sub(r'(\d+)\.375\b', r'\1-3/8', val_str)
    val_str = re.sub(r'(\d+)\.625\b', r'\1-5/8', val_str)
    val_str = re.sub(r'(\d+)\.875\b', r'\1-7/8', val_str)
    val_str = re.sub(r'(\d+)"', r'\1 in', val_str)
    val_str = re.sub(r'(\d+)\'', r'\1 ft', val_str)

    # Standardize UOM abbreviation
    uom_clean = uom.strip()
    if uom_clean in ['"', 'IN.', 'inches', 'inch', 'IN']:
        uom_clean = 'in'
    elif uom_clean in ["'", 'feet', 'foot', 'FT']:
        uom_clean = 'ft'

    # Remove duplicate unit suffixes like "60 ft in" -> "60 ft"
    if 'ft' in val_str and uom_clean == 'in':
        uom_clean = 'ft'

    return val_str, uom_clean

def normalize_attribute_list(raw_attrs: list) -> list:
    """Cleans and standardizes an extracted list of attributes."""
    normalized = []
    for label, val, uom in raw_attrs:
        c_val, c_uom = normalize_uom(val, uom)
        normalized.append((label, c_val, c_uom))
    return normalized