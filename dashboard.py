import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="PhonePe Pulse Dashboard - Insurance Map", layout="wide")
st.title("🛡️ PhonePe Pulse Insurance Map Dashboard")

def create_connection():
    return psycopg2.connect(
        host="localhost",
        user="postgres",
        password="123456",
        dbname="phonepe_pulse"
    )

@st.cache_data(ttl=600)
def load_map_insurance():
    conn = create_connection()
    df = pd.read_sql("SELECT * FROM map_insurance LIMIT 5000", conn)
    conn.close()
    return df

df = load_map_insurance()

required_cols = ['lat', 'lng']
if not all(col in df.columns for col in required_cols):
    st.error(f"Required columns {required_cols} missing in map_insurance table.")
    st.stop()

numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
numeric_cols = [col for col in numeric_cols if col not in ['lat', 'lng']]

if not numeric_cols:
    st.error("No numeric columns available for mapping.")
    st.stop()

metric = st.sidebar.selectbox("Select metric for size/color", numeric_cols)
label_cols = [col for col in df.columns if col not in ['lat', 'lng', metric]]
label = st.sidebar.selectbox("Select label for hover info", label_cols)

fig = px.scatter_mapbox(
    df,
    lat="lat",
    lon="lng",
    size=metric,
    color=metric,
    hover_name=label,
    color_continuous_scale=px.colors.sequential.Plasma,
    size_max=15,
    zoom=4,
    height=700
)

fig.update_layout(mapbox_style="carto-positron")
fig.update_layout(margin={"r":0, "t":0, "l":0, "b":0})

st.plotly_chart(fig, use_container_width=True)
