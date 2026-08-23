import re

# Comprehensive Master Catalog Brand & Manufacturer Resolution
EXPLICIT_BRAND_MAP = {
    'trex': ('Trex Company, Inc.', 'Trex®', 'Trex'),
    'timbertech': ('The AZEK Company Inc.', 'TimberTech®', 'TimberTech'),
    'dewalt': ('Stanley Black & Decker', 'DEWALT®', 'DEWALT'),
    'milwaukee': ('Milwaukee Electric Tool Corp.', 'Milwaukee®', 'Milwaukee'),
    'makita': ('Makita USA Inc.', 'Makita®', 'Makita'),
    'festool': ('Festool USA', 'Festool®', 'Festool'),
    'bosch': ('Robert Bosch Tool Corporation', 'Bosch®', 'Bosch'),
    'dremel': ('Robert Bosch Tool Corporation', 'Dremel®', 'Dremel'),
    'kreg': ('Kreg Tool Company', 'Kreg®', 'Kreg'),
    'wera': ('Wera Tools Inc.', 'Wera®', 'Wera'),
    'senco': ('Kyocera Senco Industrial Tools', 'Senco®', 'Senco'),
    'paslode': ('Illinois Tool Works Inc.', 'Paslode®', 'Paslode'),
    '3m': ('3M Company', '3M™', '3M'),
    'diablo': ('Freud America, Inc.', 'Diablo®', 'Diablo'),
    'freud': ('Freud America, Inc.', 'Freud®', 'Freud'),
    'mirka': ('Mirka Abrasives Inc.', 'Mirka®', 'Mirka'),
    'cmt': ('CMT Orange Tools USA', 'CMT®', 'CMT'),
    'whiteside': ('Whiteside Machine Company', 'Whiteside®', 'Whiteside'),
    'amana': ('Amana Tool Corporation', 'Amana Tool®', 'Amana Tool'),
    'nicholson': ('Apex Tool Group', 'Nicholson®', 'Nicholson'),
    'southwire': ('Southwire Company, LLC', 'Southwire®', 'Southwire'),
    'leviton': ('Leviton Manufacturing Co., Inc.', 'Leviton®', 'Leviton'),
    'lutron': ('Lutron Electronics Co., Inc.', 'Lutron®', 'Lutron'),
    'square d': ('Schneider Electric', 'Square D™', 'Square D'),
    'carlon': ('ABB Installation Products Inc.', 'Carlon®', 'Carlon'),
    'kichler': ('Kichler Lighting LLC', 'Kichler®', 'Kichler'),
    'satco': ('Satco Products, Inc.', 'Satco®', 'Satco'),
    'philips': ('Signify North America Corp.', 'Philips®', 'Philips'),
    'wiz': ('Signify North America Corp.', 'WiZ®', 'WiZ'),
    'feit electric': ('Feit Electric Company', 'Feit Electric®', 'Feit Electric'),
    'jameshardie': ('James Hardie Building Products', 'James Hardie®', 'James Hardie'),
    'lp smartside': ('Louisiana-Pacific Corporation', 'LP® SmartSide®', 'LP SmartSide'),
    'dsi westbury': ('DSI Westbury', 'Westbury®', 'Westbury'),
    'provia': ('ProVia LLC', 'ProVia®', 'ProVia'),
    'united window & door': ('United Window & Door', 'United®', 'United Window'),
    'hager': ('Hager Companies', 'Hager®', 'Hager'),
    'first alert': ('Resideo Technologies, Inc.', 'First Alert®', 'First Alert'),
    'brk': ('Resideo Technologies, Inc.', 'BRK®', 'BRK'),
    'hunter': ('Hunter Fan Company', 'Hunter®', 'Hunter'),
    'irwin': ('Stanley Black & Decker', 'Irwin®', 'Irwin'),
    'stealthmounts': ('StealthMounts Ltd.', 'StealthMounts®', 'StealthMounts'),
}

# Heuristics based on description keywords, manufacturer, or distinctive MPN prefixes
KEYWORD_RULES = [
    # Distinctive Brand Names in Description or Manufacturer
    (r'\bdiablo\b', 'Freud America, Inc.', 'Diablo®', 'Diablo'),
    (r'\b(freud)\b', 'Freud America, Inc.', 'Freud®', 'Freud'),
    (r'\b(cubitron|stikit|scotch-brite)\b', '3M Company', '3M™', '3M'),
    (r'\b(mirka|abranet|hiolit|iridium|deos)\b', 'Mirka Abrasives Inc.', 'Mirka®', 'Mirka'),
    (r'\b(cmt)\b', 'CMT Orange Tools USA', 'CMT®', 'CMT'),
    (r'\b(whiteside)\b', 'Whiteside Machine Company', 'Whiteside®', 'Whiteside'),
    (r'\b(amana)\b', 'Amana Tool Corporation', 'Amana Tool®', 'Amana Tool'),
    (r'\b(nicholson)\b', 'Apex Tool Group', 'Nicholson®', 'Nicholson'),
    (r'\b(milwaukee|milw|sawzall|packout)\b', 'Milwaukee Electric Tool Corp.', 'Milwaukee®', 'Milwaukee'),
    (r'\b(dewalt|de-walt)\b', 'Stanley Black & Decker', 'DEWALT®', 'DEWALT'),
    (r'\b(makita)\b', 'Makita USA Inc.', 'Makita®', 'Makita'),
    (r'\b(festool)\b', 'Festool USA', 'Festool®', 'Festool'),
    (r'\b(dremel)\b', 'Robert Bosch Tool Corporation', 'Dremel®', 'Dremel'),
    (r'\b(bosch)\b', 'Robert Bosch Tool Corporation', 'Bosch®', 'Bosch'),
    (r'\b(kreg)\b', 'Kreg Tool Company', 'Kreg®', 'Kreg'),
    (r'\b(wera)\b', 'Wera Tools Inc.', 'Wera®', 'Wera'),
    (r'\b(senco)\b', 'Kyocera Senco Industrial Tools', 'Senco®', 'Senco'),
    (r'\b(paslode)\b', 'Illinois Tool Works Inc.', 'Paslode®', 'Paslode'),
    (r'\b(prebena)\b', 'Prebena', 'Prebena®', 'Prebena'),
    (r'\b(vessel)\b', 'Vessel Tools USA', 'Vessel®', 'Vessel'),
    (r'\b(malco)\b', 'Malco Products, SBC', 'Malco®', 'Malco'),
    (r'\b(woodpeckers|align-a-saw|stealthstop)\b', 'Woodpeckers LLC', 'Woodpeckers®', 'Woodpeckers'),
    (r'\b(sawstop|saw stop)\b', 'SawStop LLC', 'SawStop®', 'SawStop'),
    (r'\b(oliver)\b', 'Oliver Machinery Co.', 'Oliver®', 'Oliver'),
    (r'\b(grizzly)\b', 'Grizzly Industrial, Inc.', 'Grizzly®', 'Grizzly'),
    (r'\b(king canada)\b', 'King Canada Inc.', 'King Canada®', 'King Canada'),
    (r'\b(jet)\b', 'JPW Industries, Inc.', 'JET®', 'JET'),
    (r'\b(trex)\b', 'Trex Company, Inc.', 'Trex®', 'Trex'),
    (r'\b(timbertech|azek)\b', 'The AZEK Company Inc.', 'TimberTech®', 'TimberTech'),
    (r'\b(hardieplank|hardiepanel|jameshardie)\b', 'James Hardie Building Products', 'James Hardie®', 'James Hardie'),
    (r'\b(smartside|smart lap|smart pan)\b', 'Louisiana-Pacific Corporation', 'LP® SmartSide®', 'LP SmartSide'),
    (r'\b(zip system|huber|advantech)\b', 'Huber Engineered Woods LLC', 'ZIP System®', 'ZIP System'),
    (r'\b(certainteed|easi-lite|firelite)\b', 'CertainTeed Gypsum', 'CertainTeed®', 'CertainTeed'),
    (r'\b(owens corning|duration trudef|weatherlock)\b', 'Owens Corning', 'Owens Corning®', 'Owens Corning'),
    (r'\b(henry|eaveguard)\b', 'Henry Company', 'Henry®', 'Henry'),
    (r'\b(westbury|dsi)\b', 'DSI Westbury', 'Westbury®', 'Westbury'),
    (r'\b(rdi|finyline|heritage post|elite post)\b', 'Barrette Outdoor Living', 'RDI®', 'RDI'),
    (r'\b(provia|ecoliteplus)\b', 'ProVia LLC', 'ProVia®', 'ProVia'),
    (r'\b(velux|skylt)\b', 'VELUX America LLC', 'VELUX®', 'VELUX'),
    (r'\b(united window|united)\b', 'United Window & Door', 'United®', 'United Window'),
    (r'\b(hager)\b', 'Hager Companies', 'Hager®', 'Hager'),
    (r'\b(southwire)\b', 'Southwire Company, LLC', 'Southwire®', 'Southwire'),
    (r'\b(leviton)\b', 'Leviton Manufacturing Co., Inc.', 'Leviton®', 'Leviton'),
    (r'\b(lutron)\b', 'Lutron Electronics Co., Inc.', 'Lutron®', 'Lutron'),
    (r'\b(square d|homeline)\b', 'Schneider Electric', 'Square D™', 'Square D'),
    (r'\b(carlon)\b', 'ABB Installation Products Inc.', 'Carlon®', 'Carlon'),
    (r'\b(halo|cooper lighting)\b', 'Cooper Lighting Solutions', 'Halo®', 'Halo'),
    (r'\b(kichler)\b', 'Kichler Lighting LLC', 'Kichler®', 'Kichler'),
    (r'\b(satco|nuvo)\b', 'Satco Products, Inc.', 'Satco®', 'Satco'),
    (r'\b(philips)\b', 'Signify North America Corp.', 'Philips®', 'Philips'),
    (r'\b(feit electric|feit)\b', 'Feit Electric Company', 'Feit Electric®', 'Feit Electric'),
    (r'\b(lithonia)\b', 'Acuity Brands Lighting, Inc.', 'Lithonia Lighting®', 'Lithonia Lighting'),
    (r'\b(streamlight)\b', 'Streamlight, Inc.', 'Streamlight®', 'Streamlight'),
    (r'\b(nebo|slyde king)\b', 'Alliance Consumer Group', 'NEBO®', 'NEBO'),
    (r'\b(first alert)\b', 'Resideo Technologies, Inc.', 'First Alert®', 'First Alert'),
    (r'\b(brk)\b', 'Resideo Technologies, Inc.', 'BRK®', 'BRK'),
    (r'\b(hunter)\b', 'Hunter Fan Company', 'Hunter®', 'Hunter'),
    (r'\b(speed queen|sq\b)\b', 'Alliance Laundry Systems LLC', 'Speed Queen®', 'Speed Queen'),
    (r'\b(frigidaire)\b', 'Electrolux Home Products', 'FRIGIDAIRE®', 'FRIGIDAIRE'),
    (r'\b(whirlpool)\b', 'Whirlpool Corporation', 'Whirlpool®', 'Whirlpool'),
    (r'\b(kitchenaid|kitchen aid)\b', 'Whirlpool Corporation', 'KitchenAid®', 'KitchenAid'),
    (r'\b(ge appliances|ge dishwasher|ge washer|ge dryer|ge microwave|ge fridge|ge range|ge cooktop|ge\b)\b', 'GE Appliances, a Haier company', 'GE®', 'GE'),
    (r'\b(cafe|café)\b', 'GE Appliances, a Haier company', 'Café™', 'Café'),
    (r'\b(lg electronics|lg dishwasher|lg washer|lg laundry|lg fridge|lg microwave|lg range|lg\b)\b', 'LG Electronics USA', 'LG®', 'LG'),
    (r'\b(beko)\b', 'Beko US Inc.', 'Beko®', 'Beko'),
    (r'\b(element)\b', 'Element Appliance Company', 'Element®', 'Element'),
    (r'\b(bow products|xtender)\b', 'Bow Products', 'Bow Products®', 'Bow Products'),
    (r'\b(rees cast stone)\b', 'Rees Cast Stone Company', 'Rees Cast Stone', 'Rees Cast Stone'),
    (r'\b(emseal)\b', 'Emseal Joint Systems Ltd', 'Emseal®', 'Emseal'),
    (r'\b(millertech)\b', 'MillerTech Energy Solutions', 'MillerTech®', 'MillerTech'),
    (r'\b(schumacher)\b', 'Schumacher Electric Corporation', 'Schumacher®', 'Schumacher'),
    (r'\b(police security)\b', 'Police Security Flashlights', 'Police Security®', 'Police Security'),
    (r'\b(u s tape|century components)\b', 'U.S. Tape Company', 'U.S. Tape®', 'U.S. Tape'),

    # Exact Multi-character MPN Prefixes
    (r'^dcb5|^dbd|^dph|^dsq|^dt[0-9]|^ddw|^d0|^d1[02]', 'Freud America, Inc.', 'Diablo®', 'Diablo'),
    (r'^3mabr|^1700-1pk', '3M Company', '3M™', '3M'),
    (r'^5b-|^9a-|^24-35m|^mid66', 'Mirka Abrasives Inc.', 'Mirka®', 'Mirka'),
    (r'^48-|^49-|^25[0-9]{2}-|^27[0-9]{2}-|^28[0-9]{2}-|^29[0-9]{2}-|^30[0-9]{2}-|^32[0-9]{2}-|^34[0-9]{2}-|^0887-|^m[127]00|^f200', 'Milwaukee Electric Tool Corp.', 'Milwaukee®', 'Milwaukee'),
    (r'^dc[bdfglmnsw][0-9]|^dw[a-z0-9]|^d2533', 'Stanley Black & Decker', 'DEWALT®', 'DEWALT'),
    (r'^x[a-z]{2}[0-9]|^bl185|^191v|^t-900', 'Makita USA Inc.', 'Makita®', 'Makita'),
    (r'^57[0-9]{4}', 'Festool USA', 'Festool®', 'Festool'),
    (r'^kpt[a-z0-9]|^bcb|^batt|^crgr', 'Kreg Tool Company', 'Kreg®', 'Kreg'),
    (r'^0513|^1331', 'Wera Tools Inc.', 'Wera®', 'Wera'),
    (r'^k527|^vb021', 'Kyocera Senco Industrial Tools', 'Senco®', 'Senco'),
    (r'^[de][0-9]+cnk', 'Prebena', 'Prebena®', 'Prebena'),
    (r'^qb22|^220usb|^ib[a-z0-9]', 'Vessel Tools USA', 'Vessel®', 'Vessel'),
    (r'^avm[67]', 'Malco Products, SBC', 'Malco®', 'Malco'),
    (r'^bc-[0-9]|^aas-|^sscms', 'Woodpeckers LLC', 'Woodpeckers®', 'Woodpeckers'),
    (r'^tg[ip]2?-|^atg[ip]-', 'SawStop LLC', 'SawStop®', 'SawStop'),
    (r'^100[0-9]{2}\.2|^4[24][0-9]{2}\.2|^10047', 'Oliver Machinery Co.', 'Oliver®', 'Oliver'),
    (r'^kc-426|^58006', 'King Canada Inc.', 'King Canada®', 'King Canada'),
    (r'^jt[19]-', 'JPW Industries, Inc.', 'JET®', 'JET'),
    (r'^543[0-9]{6}|^15137|^15168', 'Trex Company, Inc.', 'Trex®', 'Trex'),
    (r'^ad[bc]1|^agb1|^adr5|^adcr5|^15083', 'The AZEK Company Inc.', 'TimberTech®', 'TimberTech'),
    (r'^89[0-9]{5}', 'James Hardie Building Products', 'James Hardie®', 'James Hardie'),
    (r'^25796|^40503|^2582', 'Louisiana-Pacific Corporation', 'LP® SmartSide®', 'LP SmartSide'),
    (r'^hom[0-9]|^qo[0-9]', 'Schneider Electric', 'Square D™', 'Square D'),
    (r'^g19[45]|^52c|^541[57]|^52151|^72171|^wc1v|^130930|^r50003|^55418|^bha1', 'Southwire Company, LLC', 'Southwire®', 'Southwire'),
    (r'^r[0-9]{2}-|^16[15]-|^s03-|^174-|^d23lp', 'Leviton Manufacturing Co., Inc.', 'Leviton®', 'Leviton'),
    (r'^aycl-', 'Lutron Electronics Co., Inc.', 'Lutron®', 'Lutron'),
    (r'^tn[a-z0-9]|^pbuc', 'Prime Wire & Cable, Inc.', 'Prime®', 'Prime'),
    (r'^6[245]-[0-9]+|^s[1234][0-9]{3,5}', 'Satco Products, Inc.', 'Satco®', 'Satco'),
    (r'^[1345][0-9]{5}$|^603[0-9]{3}', 'Signify North America Corp.', 'Philips®', 'Philips'),
    (r'^kdfm|^kdts|^kdps|^kmmf|^kses', 'Whirlpool Corporation', 'KitchenAid®', 'KitchenAid'),
    (r'^wdts|^wsgs|^wmms|^mvwp', 'Whirlpool Corporation', 'Whirlpool®', 'Whirlpool'),
    (r'^pdsh|^pmos|^gcfg|^prfs|^pcfe', 'Electrolux Home Products', 'FRIGIDAIRE®', 'FRIGIDAIRE'),
    (r'^pdt|^pdd|^ptd|^ptw|^gde|^fcm|^gne|^pad|^pge|^pep|^ps9|^pb9|^jx', 'GE Appliances, a Haier company', 'GE®', 'GE'),
    (r'^c7cd|^c7ce|^c9tm|^c90a|^cve|^ces|^chp|^cvm', 'GE Appliances, a Haier company', 'Café™', 'Café'),
    (r'^ldph|^wke|^mser|^lsel|^lt18', 'LG Electronics USA', 'LG®', 'LG'),
    (r'^df7004|^dr[57]004|^dv2000|^dc5004|^ff7011|^tv2000|^tc5003|^tr[57]006', 'Alliance Laundry Systems LLC', 'Speed Queen®', 'Speed Queen'),
    (r'^wosp', 'Beko US Inc.', 'Beko®', 'Beko'),
    (r'^erfd|^euf', 'Element Appliance Company', 'Element®', 'Element'),
    (r'^51334|^5248|^5265|^5921|^5926|^5173', 'Hunter Fan Company', 'Hunter®', 'Hunter'),
    (r'^xt5|^xtp', 'Bow Products', 'Bow Products®', 'Bow Products'),
    (r'^d519127', 'Alliance Laundry Systems LLC', 'Speed Queen®', 'Speed Queen'),
]

def resolve_brand_row(row):
    # 1. Check if an explicit non-placeholder brand is present in the input row
    for col in ['E1_Brand', 'Unilog_Brand', 'DIB_Brand']:
        val = str(row.get(col, '')).strip().lower()
        if val and val in EXPLICIT_BRAND_MAP:
            return {
                'mfr': EXPLICIT_BRAND_MAP[val][0],
                'brand': EXPLICIT_BRAND_MAP[val][1],
                'trade': EXPLICIT_BRAND_MAP[val][2]
            }

    # 2. Check full context across MPN, description, and manufacturer text
    mpn = str(row.get('Mfg_Part_Num', '')).strip().lower()
    desc = str(row.get('Part_Desc', '')).strip().lower()
    mfr_raw = str(row.get('Clean_Manuf', '')).strip().lower()
    combined = f"{desc} {mfr_raw} {mpn}"

    for pattern, mfr, brand, trade in KEYWORD_RULES:
        if re.search(pattern, combined):
            return {'mfr': mfr, 'brand': brand, 'trade': trade}

    # Fallback to cleaned manufacturer name
    clean_mfr = row.get('Clean_Manuf', '').strip()
    brand_candidate = clean_mfr or 'Industrial'
    return {
        'mfr': clean_mfr or brand_candidate,
        'brand': brand_candidate,
        'trade': brand_candidate
    }

def run_step3(df):
    """Step 3: Resolves canonical legal manufacturer name, brand name, and trade name."""
    res = [resolve_brand_row(row) for _, row in df.iterrows()]
    df['Resolved_Mfr'] = [r['mfr'] for r in res]
    df['Resolved_Brand'] = [r['brand'] for r in res]
    df['Resolved_Trade'] = [r['trade'] for r in res]
    return df