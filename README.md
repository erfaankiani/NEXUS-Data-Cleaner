# 🧹 NEXUS Data Cleaner

A clean and user-friendly data cleaning tool built with Python, Pandas, and Streamlit.

Upload Excel or CSV files, identify common data-quality issues, remove duplicate rows, and download cleaned data in seconds.

## 📸 Preview

![NEXUS Data Cleaner](screenshots/data-cleaner-result.png)

## ✨ Features

- Upload Excel (`.xlsx`) and CSV files
- Detect duplicate rows
- Remove duplicate records
- Trim extra spaces in text columns
- Report missing values by column
- Preview data before and after cleaning
- Download cleaned files as Excel or CSV
- Simple and interactive web interface

## 🛠️ Technologies

- Python
- Pandas
- Streamlit
- OpenPyXL

## ⚙️ Installation

Install the required packages:

```bash
pip install -r requirements.txt
```

## ▶️ Run the Application

```bash
python -m streamlit run app.py
```

## 📋 Notes

- Missing values are reported but are not automatically filled or deleted.
- The tool removes duplicate rows after trimming extra spaces in text columns.
- Test the tool with a backup copy before cleaning important business data.

## 👨‍💻 Author

Erfaan Kiani