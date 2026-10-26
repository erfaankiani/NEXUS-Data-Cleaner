import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(
    page_title="NEXUS | Data Cleaner",
    page_icon="🧹",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #071426, #0b1e38);
    color: #f1f5ff;
}
[data-testid="stHeader"] {
    background: transparent;
}
[data-testid="stSidebar"] {
    background: #08172c;
    border-right: 1px solid #203858;
}
.block-container {
    padding-top: 2rem;
    max-width: 1450px;
}
h1, h2, h3 {
    color: #f1f5ff !important;
}
p, label, .stCaption {
    color: #b9c9e4;
}
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #142d52, #102440);
    border: 1px solid #294b79;
    padding: 20px;
    border-radius: 15px;
}
[data-testid="stMetricLabel"] {
    color: #c6d5ed !important;
}
[data-testid="stMetricValue"] {
    color: #ffffff !important;
}
div.stButton > button {
    background: linear-gradient(90deg, #425cff, #6755ed);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.65rem 1.2rem;
    font-weight: 600;
    width: 100%;
}
div.stButton > button:hover {
    border: 1px solid #91a7ff;
    color: white;
}
div[data-testid="stDownloadButton"] button {
    background: #12345b;
    color: white;
    border: 1px solid #4269a4;
    border-radius: 10px;
    width: 100%;
}
div[data-testid="stFileUploader"] {
    background: #102440;
    border: 1px dashed #5477ff;
    border-radius: 15px;
    padding: 15px;
}
hr {
    border-color: #263e5e;
}
.nexus-subtitle {
    color: #a9bddb;
    font-size: 16px;
}
.nexus-badge {
    display: inline-block;
    padding: 6px 12px;
    background: #173c62;
    color: #9dd8ff;
    border-radius: 20px;
    font-size: 12px;
    margin-bottom: 12px;
}
.nexus-panel {
    background: #0e2039;
    border: 1px solid #263f62;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("# 🔷 NEXUS")
    st.markdown("### Data Cleaner")
    st.caption("Clean data. Better decisions.")
    st.divider()

    st.markdown("🏠 **Home**")
    st.markdown("📤 Upload File")
    st.markdown("📊 Data Overview")
    st.markdown("🧾 Cleaning Report")
    st.markdown("📥 Download")

    st.divider()
    st.caption("NEXUS DATA TOOLS")
    st.caption("Simple tools for better data.")

st.markdown(
    '<div class="nexus-badge">DATA QUALITY TOOL</div>',
    unsafe_allow_html=True
)

st.title("🧹 NEXUS Data Cleaner")
st.markdown(
    '<p class="nexus-subtitle">'
    'Clean your Excel and CSV files in seconds. '
    'Remove duplicates, fix extra spaces, and export clean data.'
    '</p>',
    unsafe_allow_html=True
)

st.divider()

left, right = st.columns([1.6, 1])

with left:
    st.markdown("### 📤 Upload your file")
    uploaded_file = st.file_uploader(
        "Choose an Excel or CSV file",
        type=["csv", "xlsx"],
        help="Upload a file to inspect and clean."
    )

with right:
    st.markdown("### ✨ What this tool does")
    st.markdown("""
    - Removes duplicate rows
    - Trims extra spaces in text
    - Reports missing values
    - Exports cleaned Excel or CSV files
    """)

if uploaded_file is not None:
    try:
        if uploaded_file.name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Treat cells containing only spaces as missing values.
        df = df.replace(r"^\s*$", pd.NA, regex=True)

        st.divider()
        st.markdown("### 📊 Data Overview")

        original_rows = len(df)
        original_columns = len(df.columns)
        missing_cells = int(df.isna().sum().sum())

        # Trim text before detecting duplicates.
        prepared_df = df.copy()

        for column in prepared_df.select_dtypes(
            include=["object", "string"]
        ).columns:
            prepared_df[column] = prepared_df[column].apply(
                lambda value: value.strip()
                if isinstance(value, str)
                else value
            )

        duplicate_rows = int(prepared_df.duplicated().sum())

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Total Rows", f"{original_rows:,}")
        c2.metric("Total Columns", f"{original_columns:,}")
        c3.metric("Duplicate Rows", f"{duplicate_rows:,}")
        c4.metric("Missing Cells", f"{missing_cells:,}")

        st.markdown("### 👀 Original Data Preview")
        st.dataframe(
            df.head(100),
            use_container_width=True,
            height=300
        )
        st.caption("Showing up to the first 100 rows.")

        st.divider()
        st.markdown("### 🧹 Clean Your Data")

        st.info(
            "This tool removes duplicate rows and trims extra spaces. "
            "Missing values are reported, not automatically filled or deleted."
        )

        if st.button("✨ Clean My Data", use_container_width=True):
            cleaned_df = prepared_df.drop_duplicates().copy()

            removed_rows = original_rows - len(cleaned_df)
            remaining_missing = int(cleaned_df.isna().sum().sum())

            st.session_state["nexus_cleaned_df"] = cleaned_df
            st.session_state["nexus_source_name"] = uploaded_file.name
            st.session_state["nexus_removed_rows"] = removed_rows
            st.session_state["nexus_missing"] = remaining_missing

        if (
            "nexus_cleaned_df" in st.session_state
            and st.session_state.get("nexus_source_name") == uploaded_file.name
        ):
            cleaned_df = st.session_state["nexus_cleaned_df"]
            removed_rows = st.session_state["nexus_removed_rows"]
            remaining_missing = st.session_state["nexus_missing"]

            st.success("Your data has been cleaned successfully!")

            st.markdown("### 📈 Cleaning Report")

            r1, r2, r3 = st.columns(3)
            r1.metric("Rows Before", f"{original_rows:,}")
            r2.metric("Rows Removed", f"{removed_rows:,}")
            r3.metric("Rows After", f"{len(cleaned_df):,}")

            st.markdown("### 🧾 Missing Values by Column")

            missing_report = pd.DataFrame({
                "Column": cleaned_df.columns,
                "Missing Cells": [
                    int(cleaned_df[col].isna().sum())
                    for col in cleaned_df.columns
                ]
            })

            st.dataframe(
                missing_report,
                use_container_width=True,
                hide_index=True
            )

            st.markdown("### ✅ Cleaned Data Preview")
            st.dataframe(
                cleaned_df.head(100),
                use_container_width=True,
                height=300
            )

            st.divider()
            st.markdown("### 📥 Download Your Cleaned File")

            csv_data = cleaned_df.to_csv(
                index=False
            ).encode("utf-8-sig")

            excel_buffer = BytesIO()

            with pd.ExcelWriter(
                excel_buffer,
                engine="openpyxl"
            ) as writer:
                cleaned_df.to_excel(
                    writer,
                    index=False,
                    sheet_name="Cleaned Data"
                )

                missing_report.to_excel(
                    writer,
                    index=False,
                    sheet_name="Cleaning Report"
                )

            d1, d2 = st.columns(2)

            with d1:
                st.download_button(
                    "📗 Download Excel",
                    data=excel_buffer.getvalue(),
                    file_name="cleaned_data.xlsx",
                    mime=(
                        "application/vnd.openxmlformats-officedocument."
                        "spreadsheetml.sheet"
                    ),
                    use_container_width=True
                )

            with d2:
                st.download_button(
                    "📄 Download CSV",
                    data=csv_data,
                    file_name="cleaned_data.csv",
                    mime="text/csv",
                    use_container_width=True
                )

            st.caption(
                f"Cleaning complete. {remaining_missing:,} missing "
                "cells remain and have not been automatically changed."
            )

    except Exception as error:
        st.error(
            "The file could not be processed. "
            "Please check that it is a valid Excel or CSV file."
        )
        st.caption(f"Technical details: {error}")

else:
    st.markdown("""
    <div class="nexus-panel">
        <h3>🚀 Ready to clean your data?</h3>
        <p>
        Upload an Excel or CSV file to view its data quality,
        remove duplicate rows, and download a cleaned version.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.caption("NEXUS Data Cleaner | Built with Python, Pandas and Streamlit")