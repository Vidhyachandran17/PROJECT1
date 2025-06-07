import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Explore PhonePe Pulse Data", layout="wide")

def create_connection():
    return psycopg2.connect(
        host="localhost",
        user="postgres",
        password="123456",
        dbname="phonepe_pulse"
    )

def load_data(table_name):
    query = f"SELECT * FROM {table_name} LIMIT 1000"
    conn = create_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

st.title("📂 PhonePe Pulse Data Explorer")

tables = [
    "aggregated_transaction",
    "aggregated_user",
    "map_transaction",
    "map_user",
    "top_transaction",
    "top_user",
    "aggregated_insurance",
    "top_insurance",
    "map_insurance"
]

selected_table = st.selectbox("Select Table", tables)

df = load_data(selected_table)

if df.empty:
    st.warning("No data available in this table.")
    st.stop()

numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

if not numeric_cols:
    st.warning("No numeric columns found for plotting.")
    st.stop()

selected_metric = st.selectbox("Select Numeric Field", numeric_cols)

if all(col in df.columns for col in ['lat', 'lng']):
    st.subheader(f"Map Plot of {selected_metric}")
    fig = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lng",
        size=selected_metric,
        color=selected_metric,
        hover_name=df.columns[0],
        color_continuous_scale=px.colors.sequential.Plasma,
        size_max=15,
        zoom=4,
        height=500
    )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    st.plotly_chart(fig, use_container_width=True)
else:
    st.subheader(f"Scatter Plot of {selected_metric}")
    fig = px.scatter(
        df,
        x=df.index,
        y=selected_metric,
        labels={"x": "Index", "y": selected_metric},
        title=f"Scatter Plot of {selected_metric}"
    )
    st.plotly_chart(fig, use_container_width=True)
