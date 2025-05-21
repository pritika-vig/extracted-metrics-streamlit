import streamlit as st
import requests
from urllib.parse import urljoin

# Configuration
BUCKET_URL = "https://storage.googleapis.com/patient-engagement-pipeline-bucket/extracted_text/pubmed_search/20250521_145659/"
FILE_LIST_URL = BUCKET_URL + "file_list.json"

st.set_page_config(page_title="Patient Engagement Viewer", layout="wide")
st.title("🧾 Patient Engagement Paper Viewer")

# Load list of JSON filenames
try:
    res = requests.get(FILE_LIST_URL)
    res.raise_for_status()
    json_files = res.json()
except Exception as e:
    st.error(f"Could not load file list: {e}")
    st.stop()

# Dropdown to select a file
selected_file = st.selectbox("Choose a paper file", json_files)

if selected_file:
    file_url = urljoin(BUCKET_URL, selected_file)
    st.markdown(f"🔗 **Loading file:** [{selected_file}]({file_url})")

    # Try to fetch and parse JSON
    try:
        response = requests.get(file_url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        st.error(f"Failed to load or parse JSON: {e}")
        st.text(response.text[:500])  # optional debug
        st.stop()

    # Display paper-level metadata
    st.subheader("📄 Paper Info")
    st.markdown(f"**Title:** `{data.get('paper_title', 'N/A')}`")
    source_url = data.get('source_url')
    if source_url:
        st.markdown(f"[🔗 View on PubMed]({source_url})")

    # Display fields
    st.subheader("📑 Extracted Fields")
    for field in data.get("fields", []):
        with st.expander(f"🧩 {field.get('name', 'Unnamed Field')}"):
            st.markdown(f"**Description:** {field.get('description', 'N/A')}")
            st.markdown(f"**Value:** {field.get('value', 'N/A')}")
            st.markdown(f"**Evidence Quote:** {field.get('evidence_quote', 'N/A')}")
            st.markdown(f"**Page Number:** {field.get('page_number', 'N/A')}")
