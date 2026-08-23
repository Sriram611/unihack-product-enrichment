import streamlit as st
import pandas as pd
import tempfile
import os

from step1_ingest import ingest_dataset
from step2_preprocess import run_step2
from step3_resolution import run_step3
from step4_scraper import enrich_with_urls
from step5_classification import run_step5
from step8_descriptions import build_descriptions
from step9_output_formatter import OUTPUT_COLUMNS

st.set_page_config(page_title="UniHack Enrichment Pipeline", page_icon="🏭", layout="wide")

st.title("🏭 Industrial Product Enrichment Engine")
st.markdown("Automated Enrichment, Attribute Extraction, Brand Resolution & Content Pipeline.")

uploaded_file = st.file_uploader("Upload raw product dataset (CSV or XLSX)", type=['csv', 'xlsx'])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    df_raw = ingest_dataset(tmp_path)
    st.subheader(f"Input Data Preview ({len(df_raw)} items)")
    st.dataframe(df_raw.head(5))

    if st.button("🚀 Run Complete Enrichment Workflow"):
        progress_bar = st.progress(0)
        status_text = st.empty()

        status_text.text("Step 2/9: Preprocessing & Placeholder Removal...")
        df = run_step2(df_raw)
        progress_bar.progress(20)

        status_text.text("Step 3/9: Normalizing Manufacturers & Canonical Brands...")
        df = run_step3(df)
        progress_bar.progress(40)

        status_text.text("Step 4/9: Sourcing Official Manufacturer URLs & Reference PDFs...")
        df = enrich_with_urls(df)
        progress_bar.progress(60)

        status_text.text("Step 5/9: Classifying Taxonomy & Categorization...")
        df = run_step5(df)
        progress_bar.progress(80)

        status_text.text("Steps 6-8/9: Building Attributes & Descriptions...")
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

        out_df = pd.DataFrame(rows)
        for col in OUTPUT_COLUMNS:
            if col not in out_df.columns:
                out_df[col] = ''
        out_df = out_df[OUTPUT_COLUMNS].fillna('')
        progress_bar.progress(100)
        status_text.success("🎉 Enrichment Complete!")

        # KPI Metrics
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Brand Resolution", f"{(out_df['BRAND_NAME'] != '').sum()} / {len(out_df)}")
        c2.metric("Sourced URLs", f"{(out_df['MFR URL'] != '').sum()} / {len(out_df)}")
        c3.metric("Invoice Desc ≤40 Chars", f"{(out_df['INVOICE_DESC'].str.len() <= 40).sum()} / {len(out_df)}")
        c4.metric("Attributes Populated", f"{(out_df['ATTRIBUTE_LABEL 1'] != '').sum()} / {len(out_df)}")

        st.subheader("Enriched Delivery Table (252 Static Columns)")
        st.dataframe(out_df[['Mfg_Part_Num', 'MANUFACTURER_NAME', 'BRAND_NAME', 'Classpath', 'INVOICE_DESC', 'MOBILE_DESC', 'SHORT_DESC', 'MFR URL']].head(20))

        csv_data = out_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Expected Delivery Format CSV (252 Columns)",
            data=csv_data,
            file_name="enriched_output_delivery.csv",
            mime="text/csv"
        )