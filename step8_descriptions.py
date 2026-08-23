import re
from step6_attributes import extract_raw_attributes
from step7_normalization import normalize_attribute_list

def truncate_text(text: str, limit: int) -> str:
    """Truncates cleanly at a word boundary within character limits."""
    text = text.strip()
    if len(text) <= limit:
        return text
    truncated = text[:limit]
    last_space = truncated.rfind(' ')
    if last_space > int(limit * 0.6):
        return truncated[:last_space].strip()
    return truncated.strip()

def build_descriptions(row):
    """Step 8: Generates five distinct tiers of descriptions adhering to formula rules."""
    mpn = str(row.get('Mfg_Part_Num', '')).strip()
    desc = str(row.get('Part_Desc', '')).strip()
    mfr = str(row.get('Resolved_Mfr', '')).strip()
    brand = str(row.get('Resolved_Brand', '')).strip()
    pname = str(row.get('Product_Name', '')).strip()

    # Extract & normalize attributes
    raw_attrs = extract_raw_attributes(desc)
    attrs = normalize_attribute_list(raw_attrs)
    attr_dict = {label: (val, uom) for label, val, uom in attrs}

    # 1. INVOICE_DESC (<=40 chars, UPPERCASE)
    inv_tokens = [pname.upper()]
    for label in ['Grit', 'Dimensions', 'Size', 'Voltage Rating', 'Material', 'Color']:
        if label in attr_dict:
            inv_tokens.append(str(attr_dict[label][0]).upper().replace(' IN', 'IN'))
    invoice_desc = truncate_text(' '.join(inv_tokens), 40)

    # 2. MOBILE_DESC (60-80 chars)
    mob_parts = [mfr, brand, pname, mpn]
    for label in ['Dimensions', 'Grit', 'Voltage Rating']:
        if label in attr_dict:
            mob_parts.append(str(attr_dict[label][0]))
    mobile_str = ', '.join([p for p in mob_parts if p])
    if len(mobile_str) > 80:
        mobile_desc = truncate_text(mobile_str, 80)
    elif len(mobile_str) < 60:
        mobile_desc = f"{mfr} {brand} {pname} Model {mpn}".strip()
    else:
        mobile_desc = mobile_str

    # 3. SHORT_DESC (Brand + MPN + Product Name + Key Specs)
    short_parts = [brand, mpn, pname]
    for label in ['Dimensions', 'Grit', 'Voltage Rating', 'Material']:
        if label in attr_dict:
            short_parts.append(str(attr_dict[label][0]))
    short_desc = ' '.join([p for p in short_parts if p])

    # 4. LONG_DESC1 (Brand Product Name, specs..., Part Number)
    long_items = [f"{brand} {pname}"]
    for label, val, uom in attrs:
        long_items.append(f"{val} {uom}".strip() if uom and not val.endswith(uom) else val)
    long_desc = ', '.join(long_items) + f", Part Number: {mpn}"

    # 5. Image & Technical Spec Sheet
    brand_clean = re.sub(r'[®™]', '', brand).replace(' ', '_')
    image_name = f"{brand_clean}_{mpn}.jpg" if mpn else "product_image.jpg"
    spec_sheet_name = f"{brand_clean}_{mpn}_Specification_Sheet.pdf" if mpn else ""

    out = {
        'Product Name': pname,
        'MOBILE_DESC': mobile_desc,
        'INVOICE_DESC': invoice_desc,
        'SHORT_DESC': short_desc,
        'LONG_DESC1': long_desc,
        'RETAIL_DESC': short_desc,
        'MARKETING_DESCRIPTION': f"High performance {brand} {pname} engineered for industrial, commercial, and professional applications.",
        'ITEM_FEATURES_1': f"Engineered by {brand} for high durability and performance.",
        'ITEM_FEATURES_2': f"Compatible with standard {pname} operations.",
        'ITEM_FEATURES_3': f"Manufacturer Part Number: {mpn}",
        'Product Image': image_name,
        'Specification Sheet': spec_sheet_name,
        'Actual Image (Yes/No)': 'Yes',
        'Discontinued': 'No',
        'Standard Packaging Information': '1'
    }

    # Populate 50 attribute slot triples (ATTRIBUTE_LABEL, ATTRIBUTE_VALUE, ATTRIBUTE_UOM)
    for i in range(1, 51):
        if i <= len(attrs):
            out[f'ATTRIBUTE_LABEL {i}'] = attrs[i-1][0]
            out[f'ATTRIBUTE_VALUE {i}'] = attrs[i-1][1]
            out[f'ATTRIBUTE_UOM {i}'] = attrs[i-1][2]
        else:
            out[f'ATTRIBUTE_LABEL {i}'] = ''
            out[f'ATTRIBUTE_VALUE {i}'] = ''
            out[f'ATTRIBUTE_UOM {i}'] = ''

    return out