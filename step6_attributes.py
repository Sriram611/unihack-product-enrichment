import re

def extract_raw_attributes(desc: str) -> list:
    """Step 6: Extracts domain-specific key-value attribute candidates from product text."""
    attrs = []
    desc_str = str(desc)

    # Electrical Specs
    v = re.search(r'\b(\d+(?:\.\d+)?)\s*V(?:olts?)?\b', desc_str, re.I)
    if v: attrs.append(('Voltage Rating', v.group(1), 'V'))

    a = re.search(r'\b(\d+(?:\.\d+)?)\s*A(?:mps?)?\b', desc_str, re.I)
    if a: attrs.append(('Amperage Rating', a.group(1), 'A'))

    w = re.search(r'\b(\d+(?:\.\d+)?)\s*W(?:atts?)?\b', desc_str, re.I)
    if w: attrs.append(('Power Rating', w.group(1), 'W'))

    ah = re.search(r'\b(\d+(?:\.\d+)?)\s*(?:Ah|AH)\b', desc_str, re.I)
    if ah: attrs.append(('Battery Capacity', ah.group(1), 'Ah'))

    # Tool & Abrasive Specs
    grit = re.search(r'\b(?:P(\d+)|(\d+)\s*Grit)\b', desc_str, re.I)
    if grit:
        g = grit.group(1) or grit.group(2)
        attrs.append(('Grit', f"P{g}" if not g.startswith('P') else g, 'Grit'))

    teeth = re.search(r'\b(\d+)\s*(?:T|Tooth|Teeth)\b', desc_str, re.I)
    if teeth: attrs.append(('Number of Teeth', teeth.group(1), ''))

    qty = re.search(r'\b(\d+)\s*(?:pc|pcs|pk|pack|box|disc/box|sheets/box)\b', desc_str, re.I)
    if qty: attrs.append(('Package Quantity', qty.group(1), 'pcs'))

    # Dimensions
    dim_multi = re.search(r'((?:\d+(?:-\d+/\d+|\.\d+|/\d+)?(?:"|\')?\s*x\s*)+(?:\d+(?:-\d+/\d+|\.\d+|/\d+)?(?:"|\')?))', desc_str, re.I)
    if dim_multi:
        attrs.append(('Dimensions', dim_multi.group(1), 'in'))
    else:
        single_dim = re.search(r'(\d+(?:-\d+/\d+|\.\d+|/\d+)?)\s*(?:in|\"|\'|ft)\b', desc_str, re.I)
        if single_dim:
            attrs.append(('Size', single_dim.group(0), 'in'))

    # Materials
    if re.search(r'\b(SS|Stainless Steel)\b', desc_str, re.I):
        attrs.append(('Material', 'Stainless Steel', ''))
    elif re.search(r'\b(Brass|BRS)\b', desc_str, re.I):
        attrs.append(('Material', 'Brass', ''))
    elif re.search(r'\b(Aluminum|Alum)\b', desc_str, re.I):
        attrs.append(('Material', 'Aluminum', ''))
    elif re.search(r'\b(PVC)\b', desc_str, re.I):
        attrs.append(('Material', 'PVC', ''))

    # Colors
    if re.search(r'\b(Black|Blk|Bk)\b', desc_str, re.I):
        attrs.append(('Color', 'Black', ''))
    elif re.search(r'\b(White|Wh)\b', desc_str, re.I):
        attrs.append(('Color', 'White', ''))

    return attrs