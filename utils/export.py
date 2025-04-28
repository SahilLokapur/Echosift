import pandas as pd
import streamlit as st
import json

def export_data(data):
    df = pd.DataFrame([data])
    st.download_button("Download as CSV", df.to_csv(index=False), "data.csv")
    st.download_button("Download as JSON", json.dumps(data), "data.json")
