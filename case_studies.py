import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px

# ---------- Database Connection ----------
def create_connection():
    return psycopg2.connect(
        host="localhost",
        user="postgres",
        password="123456",
        dbname="phonepe_pulse"
    )

# ---------- Case Study Rendering ----------
def run_case_studies():
    st.title("📊 PhonePe Pulse Case Studies")

    case = st.selectbox("Select a Case Study", [
        "1. Decoding Transaction Dynamics",
        "2. Device Dominance and User Engagement",
        "3. Insurance Penetration and Growth Potential",
        "4. Transaction Analysis for Market Expansion",
        "5. User Engagement and Growth Strategy"
    ])

    conn = create_connection()

    # ---------- Case Study 1 ----------
    if case.startswith("1"):
        st.header("1. Decoding Transaction Dynamics")
        df = pd.read_sql("""
            SELECT state, year, quarter, transaction_type, 
                   transaction_count AS count, 
                   transaction_amount AS amount 
            FROM aggregated_transaction
        """, conn)

        state_summary = df.groupby('state')[['count', 'amount']].sum().reset_index().sort_values(by='amount', ascending=False)
        fig = px.bar(state_summary, x='state', y='amount', title='Total Transaction Amount by State')
        st.plotly_chart(fig, use_container_width=True)

        st.write("📌 **Insight:** States with higher transaction volume and value show strong digital adoption. Low-performing regions might need targeted awareness or infrastructure.")

    # ---------- Case Study 2 ----------
    elif case.startswith("2"):
        st.header("2. Device Dominance and User Engagement")
        df = pd.read_sql("""
            SELECT state, year, quarter, registered_users, app_opens 
            FROM aggregated_user
        """, conn)

        state_summary = df.groupby('state')[['registered_users', 'app_opens']].sum().reset_index()
        fig = px.bar(state_summary, x='state', y='registered_users', title='Registered Users by State')
        st.plotly_chart(fig, use_container_width=True)

        st.write("📌 **Insight:** Compare user registrations vs. app opens across states. Some states might have underutilization or engagement gaps.")

    # ---------- Case Study 3 ----------
    elif case.startswith("3"):
        st.header("3. Insurance Penetration and Growth Potential")
        df = pd.read_sql("""
            SELECT state, year, quarter, insurance_type, 
                   insurance_count AS count, 
                   insurance_amount AS amount 
            FROM aggregated_insurance
        """, conn)

        insurance_summary = df.groupby('state')[['count', 'amount']].sum().reset_index().sort_values(by='count', ascending=False)
        fig = px.bar(insurance_summary, x='state', y='count', title='Total Insurance Transactions by State')
        st.plotly_chart(fig, use_container_width=True)

        st.write("📌 **Insight:** High insurance activity in certain states signals maturity. Lower penetration indicates growth opportunity.")

    # ---------- Case Study 4 ----------
    elif case.startswith("4"):
        st.header("4. Transaction Analysis for Market Expansion")
        df = pd.read_sql("""
            SELECT state, year, quarter, transaction_type, 
                   transaction_count AS count, 
                   transaction_amount AS amount 
            FROM aggregated_transaction
        """, conn)

        trend_df = df.groupby(['year', 'quarter'])[['count', 'amount']].sum().reset_index()
        fig = px.line(trend_df, x='quarter', y='count', color='year', markers=True, title='Quarterly Transactions Over Years')
        st.plotly_chart(fig, use_container_width=True)

        st.write("📌 **Insight:** Seasonal spikes can guide campaign timings. States with consistent growth are ripe for deeper market investments.")

    # ---------- Case Study 5 ----------
    elif case.startswith("5"):
        st.header("5. User Engagement and Growth Strategy")
        df = pd.read_sql("""
            SELECT state, year, quarter, registered_users, app_opens 
            FROM aggregated_user
        """, conn)

        engagement_df = df.groupby('state')[['registered_users', 'app_opens']].sum().reset_index()
        fig = px.scatter(engagement_df, x='registered_users', y='app_opens', size='app_opens', color='state', title='User Engagement: App Opens vs Registrations')
        st.plotly_chart(fig, use_container_width=True)

        st.write("📌 **Insight:** Disparity between registrations and app opens may indicate user drop-off or app engagement gaps.")

    conn.close()
