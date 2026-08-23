import sys
import os
import pandas as pd
from datetime import datetime

# Guarantee local directory is on python search path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from step1_ingest import ingest_dataset
from step2_preprocess import run_step2
from step3_resolution import run_step3
from step4_scraper import enrich_with_urls
from step5_classification import run_step5
from step8_descriptions import build_descriptions
from step9_output_formatter import write_delivery_csv

def run_enrichment_pipeline(input_path: str, output_path: str = None) -> str:
    print("🏭 Starting UniHack 9-Stage Product Enrichment Pipeline...")
    print("=" * 60)

    # Step 1: Ingest & Deduplicate
    df = ingest_dataset(input_path)

    # Step 2: Preprocess & Filter Placeholders
    print("🧹 Step 2: Preprocessing raw strings & filtering placeholders...")
    df = run_step2(df)

    # Step 3: Canonical Brand & Manufacturer Resolution
    print("🏷️  Step 3: Resolving Brands & Manufacturers...")
    df = run_step3(df)

    # Step 4: Sourcing Manufacturer URLs
    print("🌐 Step 4: Sourcing Official Manufacturer Links & PDFs...")
    df = enrich_with_urls(df)

    # Step 5: Taxonomy Classification
    print("📂 Step 5: Classifying Taxonomy & Classpath...")
    df = run_step5(df)

    # Steps 6, 7, 8: Attributes, Normalization & Descriptions
    print("🧠 Steps 6-8: Extracting Attributes, Normalizing UOMs & Building Descriptions...")
    rows = []
    for _, row in df.iterrows():
        enriched = build_descriptions(row)
        record = {}
        for col in ['PART_NUMBER', 'Dept', 'Class', 'Fine', 'SKU - MY_PART_NUMBER',
                    'Mfg_Part_Num', 'Part_Desc', 'E1_Brand', 'Unilog_Brand', 'DIB_Brand', 'Part_Manuf']:
            record[col] = row.get(col, '')

        record['MFR URL'] = row.get('MFR URL', '')
        for i in range(1, 6):
            record[f'Ref URL {i}'] = row.get(f'Ref URL {i}', '')

        record['MANUFACTURER_NAME'] = row.get('Resolved_Mfr', '')
        record['BRAND_NAME'] = row.get('Resolved_Brand', '')
        record['TRADE_NAME'] = row.get('Resolved_Trade', '')
        record['MANUFACTURER_PART_NUMBER'] = row.get('Mfg_Part_Num', '')
        record['Classpath'] = row.get('Classpath', '')
        record.update(enriched)
        rows.append(record)

    # Step 9: Package 252 Columns
    if not output_path:
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f"enriched_output_{ts}.csv"

    print("📦 Step 9: Formatting & exporting final 252-column CSV...")
    write_delivery_csv(rows, output_path)

    # Metric summary for judges
    n = len(rows)
    brands_resolved = sum(1 for r in rows if r.get('BRAND_NAME'))
    urls_covered = sum(1 for r in rows if r.get('MFR URL'))
    inv_compliant = sum(1 for r in rows if len(r.get('INVOICE_DESC', '')) <= 40)
    classified = sum(1 for r in rows if r.get('Classpath') and 'General Industrial' not in r.get('Classpath'))

    print("\n" + "=" * 60)
    print("📊 UNIHACK PIPELINE KPI REPORT:")
    print(f"  • Brand & Mfr Resolution: {brands_resolved}/{n} ({100*brands_resolved/n:.1f}%)")
    print(f"  • Taxonomy Classification: {classified}/{n} ({100*classified/n:.1f}%)")
    print(f"  • Official URL Sourcing:   {urls_covered}/{n} ({100*urls_covered/n:.1f}%)")
    print(f"  • Invoice Desc (<=40 char): {inv_compliant}/{n} ({100*inv_compliant/n:.1f}%)")
    print("=" * 60)

    return output_path

if __name__ == '__main__':
    target_file = sys.argv[1] if len(sys.argv) > 1 else 'Unihack_ Sample Dataset - Input.csv'
    if not os.path.exists(target_file):
        for candidate in ['input.csv', 'Sample-1000_Items.xlsx']:
            if os.path.exists(candidate):
                target_file = candidate
                break
    run_enrichment_pipeline(target_file)