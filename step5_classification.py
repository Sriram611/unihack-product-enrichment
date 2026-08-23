import re

TAXONOMY_RULES = [
    # Power Saws & Cutters (Evaluated before general grip/disc patterns)
    (r'\b(circular saw|circ saw|circ - saw|jig saw|jigsaw|miter saw|recip saw|table saw|bandsaw|track saw)\b', 'Tools & Hardware > Power Tools > Saws', 'Power Saw'),

    # Abrasives & Cutting Tools
    (r'\b(sanding belt|sander belt|sanding sponge)\b', 'Tools & Hardware > Abrasives > Sanding Belts & Sheets', 'Sanding Belt'),
    (r'\b(cut-off|cut off|cutoff disc|cutoff wheel|cut and grind|cut n grind)\b', 'Tools & Hardware > Abrasives > Cut-Off Wheels', 'Cut-Off Disc'),
    (r'\b(grinding wheel|grind disc)\b', 'Tools & Hardware > Abrasives > Grinding Wheels', 'Grinding Wheel'),
    (r'\b(film disc|stikit|cubitron|abranet|hiolit|sanding disc|abrasive set|delta s gr|iridium grip|systainer abrasive|gr pro)\b', 'Tools & Hardware > Abrasives > Sanding Discs & Sheets', 'Abrasive Disc'),
    (r'\b(circ saw blade|saw blade|blade|dado|jig saw blade|sawzall blade|track saw blade|framing blade|diamond blade|tile blade|tile - blade|planer blade|planer knives|file bstd|tfrming)\b', 'Tools & Hardware > Saw Blades & Accessories > Circular & Reciprocating Blades', 'Saw Blade'),
    (r'\b(router bit|cutter|shaper|countersink|hole dozer|drill bit|plug cutter)\b', 'Tools & Hardware > Cutting Tools > Router & Drill Bits', 'Router Bit'),
    (r'\b(drive bit|torx drive|phillips drive|square drive|screw setter|bit set|torsion bit|socket adapter|universal joint|ratchet & socket|wrench set|bit holder)\b', 'Tools & Hardware > Fastening Tools > Bits, Sockets & Wrenches', 'Fastening Tool / Bit'),

    # Power Tools & Machinery
    (r'\b(drill driver|hammer drill|impact driver|impact wrench|drill press|hydraulic driver|driver drill|drill)\b', 'Tools & Hardware > Power Tools > Drills & Drivers', 'Drill / Impact Driver'),
    (r'\b(nailer|stapler|grease gun|heat gun|die grinder|angle grinder|grinder|planer|jointer|shaper|stock feeder|rotary tool|band file|polisher|sander|blower|string trimmer|hedge trimmer)\b', 'Tools & Hardware > Power Tools > Specialty Power Tools', 'Power Tool'),
    (r'\b(battery|powerpack|starter kit|charger|power source|power supply)\b', 'Tools & Hardware > Power Tool Accessories > Batteries & Chargers', 'Battery / Charger'),
    (r'\b(dust extractor|paper bag|vacuum)\b', 'Tools & Hardware > Power Tool Accessories > Dust Management & Vacuums', 'Dust Extractor / Vacuum'),
    (r'\b(fence|miter sled|zero-clearance|align-a-saw|stand support|magazine|collated attach|shears replacement)\b', 'Tools & Hardware > Power Tool Accessories > Tool Attachments & Fences', 'Power Tool Accessory'),
    (r'\b(tool chest|organizer|carrying bit holder)\b', 'Tools & Hardware > Tool Storage > Boxes & Organizers', 'Tool Storage'),
    (r'\b(laser|laser level|voltage detector|rafter square|raftersquare|bigcal|t-square|folding knife|snip|chalk & reel|pencil|holster|bottle|gauge|kneeling pad)\b', 'Tools & Hardware > Hand Tools & Measuring > Layout & Measuring Tools', 'Hand Tool / Measuring Device'),

    # Building Materials & Decking
    (r'\b(decking|sq edge|grooved|fascia)\b', 'Building Materials > Decking & Railing > Composite Decking & Fascia', 'Decking Board / Fascia'),
    (r'\b(rail kit|post trim|post sleeve|post cap|gate|baluster|post wrap|support post|ada rail|ada wall|end cap|rail panel)\b', 'Building Materials > Decking & Railing > Railing Systems & Components', 'Railing Component'),
    (r'\b(patio dr|slider|window|skylt|skylight|hopper|access door|threshold)\b', 'Building Materials > Windows & Doors > Windows & Doors', 'Window / Door'),
    (r'\b(drywall|sheathing|osb|sub floor|rainscreen|mortar|joist tape|insulation|easi-lite|firelite)\b', 'Building Materials > Structural & Wall Materials > Sheathing & Panels', 'Building Material / Panel'),
    (r'\b(premier rib|shingle|duration trudef|ice guard|eaveguard)\b', 'Building Materials > Roofing & Siding > Roofing & Siding Panels', 'Roofing / Siding'),
    (r'\b(finish nail|staple|fastener)\b', 'Building Materials > Fasteners & Hardware > Nails & Staples', 'Fasteners'),

    # Electrical & Lighting
    (r'\b(chandelier|pendant|wall sconce|wall light|ceiling light|bath light|downlight|down light|strip light|highbay|wrap light|shop light|motion lt|flat panel|ext wall lt|post lt|work light|headlight|flashlight|lantern)\b', 'Electrical & Lighting > Luminaires & Fixtures > Indoor & Outdoor Lighting', 'Light Fixture'),
    (r'\b(led bulb|bulb|halogen|incan|lamp|sodium med)\b', 'Electrical & Lighting > Lamps & Bulbs > LED & Specialty Lamps', 'Light Bulb'),
    (r'\b(dimmer|timer|switch|receptacle|outlet|wallplate|load center|load cntr|enclosure|box cover|oct box|square box|2g box|decor plate|wall tap|cord conn)\b', 'Electrical & Lighting > Wiring Devices & Electrical Boxes', 'Electrical Wiring Device'),
    (r'\b(cable|wire|cord|triplex|cord grip|cat5e|elect tape|vinyl elect tape|tape light)\b', 'Electrical & Lighting > Wire & Cable > Electrical Conductors & Tape', 'Electrical Wire / Tape'),

    # Major Appliances
    (r'\b(dishwasher)\b', 'Appliances & Consumer Electronics > Kitchen Appliances > Built-In Dishwashers', 'Dishwasher'),
    (r'\b(dryer)\b', 'Appliances & Consumer Electronics > Laundry Appliances > Clothes Dryers', 'Dryer'),
    (r'\b(washer)\b', 'Appliances & Consumer Electronics > Laundry Appliances > Washing Machines', 'Washing Machine'),
    (r'\b(laundry center)\b', 'Appliances & Consumer Electronics > Laundry Appliances > Laundry Centers', 'Laundry Center'),
    (r'\b(microwave|drawer ss)\b', 'Appliances & Consumer Electronics > Cooking Appliances > Microwaves', 'Microwave'),
    (r'\b(range|cooktop|wall oven)\b', 'Appliances & Consumer Electronics > Cooking Appliances > Ranges & Ovens', 'Range / Cooktop'),
    (r'\b(fridge|refrigerator|freezer|beverage center)\b', 'Appliances & Consumer Electronics > Refrigeration > Refrigerators & Freezers', 'Refrigerator / Freezer'),
    (r'\b(coffee maker|espresso|toaster|toast oven|heater kit|range grill)\b', 'Appliances & Consumer Electronics > Small Appliances > Countertop Appliances', 'Countertop Appliance'),
    (r'\b(fan|ceiling fan)\b', 'Appliances & Consumer Electronics > Residential Fans > Ceiling Fans', 'Ceiling Fan'),

    # Safety & Security
    (r'\b(safety glasses|eyewear)\b', 'Safety & Security > Personal Protective Equipment > Eye Protection', 'Safety Glasses'),
    (r'\b(heated glove|hoodie|heated jacket|liners|hearing protector)\b', 'Safety & Security > Workwear & Personal Safety > Safety Apparel', 'Safety Apparel'),
    (r'\b(fire extinguisher|smoke & co alarm|driveway alert)\b', 'Safety & Security > Emergency & Fire Safety > Alarms & Extinguishers', 'Safety Device')
]

def classify_product(desc: str, mfr: str = ''):
    text = f"{desc} {mfr}".lower()
    for pattern, classpath, prod_name in TAXONOMY_RULES:
        if re.search(pattern, text):
            return classpath, prod_name
    return 'Industrial Supplies & Equipment > Maintenance, Repair & Operations', 'Industrial Equipment'

def run_step5(df):
    """Step 5: Maps every product to the taxonomy hierarchy and canonical product name."""
    cps, pnames = [], []
    for _, row in df.iterrows():
        desc = str(row.get('Part_Desc', ''))
        mfr = str(row.get('Clean_Manuf', ''))
        cp, pname = classify_product(desc, mfr)
        cps.append(cp)
        pnames.append(pname)
    df['Classpath'] = cps
    df['Product_Name'] = pnames
    return df