# app.py
import streamlit as st
import pandas as pd
from agents.detection_agent import DataIngestionAgent, IncidentDetectionAgent
from agents.response_agent import ResponsePlannerAgent
from agents.communication_agent import CommunicationAgent
from agents.rag_agent import RAGAgent

# ----------------------------- PAGE CONFIG --------------------------------
st.set_page_config(page_title="NexGen LiveOps", layout="wide")
st.title("🚚 NexGen LiveOps — Real-Time Incident Intelligence Dashboard")

# ----------------------------- DATA LOADING --------------------------------


use_local = True

if use_local:
    ing = DataIngestionAgent(data_dir="data")
    master = ing.load_all()
else:
    st.warning("Please upload CSVs manually if not using local folder.")
    st.stop()

# ----------------------------- MASTER PREVIEW --------------------------------
col1, col2 = st.columns([2, 1])
with col1:
    st.header("📦 Master Data Preview")
    st.dataframe(master.head(200))

with col2:
    st.header("📊 Quick KPIs")
    total_orders = len(master)
    st.metric("Total Orders", total_orders)
    if "Rating" in master.columns:
        low_ratings = master[master["Rating"] <= 2].shape[0]
        st.metric("Low-Rating Orders", low_ratings)
    if "Total_Cost" in master.columns:
        st.metric("Avg Total Cost (INR)", f"{master['Total_Cost'].mean():,.2f}")

st.markdown("---")

# ----------------------------- INCIDENT DETECTION --------------------------------
st.header("🧠 Incident Detection & Response Planning")

if st.button("Run Detection & Plan Responses"):
    detector = IncidentDetectionAgent(master)
    basic_inc = detector.flag_basic_incidents(delay_days_threshold=2)
    anomalies = detector.anomaly_detection()

    st.subheader("Detected Incidents")
    st.write(f"Total Incidents Found: {len(detector.incidents)}")
    st.dataframe(detector.incidents.head(200))

    # Response Planning
    fleet_df = ing.fleet if hasattr(ing, "fleet") else pd.DataFrame()
    planner = ResponsePlannerAgent(detector.incidents, fleet_df)
    plans = planner.plan_response(detector.incidents)

    st.subheader("Suggested Response Plans")
    st.dataframe(plans.head(200))

    st.success(f"✅ {len(plans)} incident response plans generated successfully.")
    st.caption("You can now query specific orders or incidents below using the Gemini Assistant.")

    # Store state
    st.session_state["detector"] = detector
    st.session_state["planner"] = planner

st.markdown("---")

# ----------------------------- GEMINI CHAT --------------------------------
st.header("💬 Gemini Assistant — Ask About Orders or Issues")

# Instantiate RAG Agent once
if "rag" not in st.session_state:
    st.session_state["rag"] = RAGAgent(master)

query = st.text_input(
    "Ask a question (e.g. 'Why is Order_ID 142 delayed?' or 'Which customer complained about damaged items?')"
)
use_llm = st.checkbox("Use Gemini (requires GEMINI_API_KEY)", value=True)

if st.button("Ask") and query.strip():
    rag = st.session_state["rag"]
    retrieved = rag.retrieve(query, top_k=4)
    out = rag.generate_answer(query, retrieved, use_llm=use_llm)

    st.markdown(
        f"""
        <div style='background-color:#1e293b; color:white; padding:1.2em; border-radius:12px;'>
        <h4>Gemini's Analysis</h4>
        <p style='font-size:15px; line-height:1.6;'>{out['answer']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("🔍 Retrieved Data Context (Top Matches)"):
        for r in retrieved:
            st.write(f"**Order {r['row'].get('Order_ID', 'N/A')}** — Score {r['score']:.3f}")
            snippet = str(r['row'].get('Feedback_Text', ''))[:300]
            st.caption(snippet)

st.markdown("---")
st.caption("© 2025 NexGen LiveOps — AI-powered Logistics Intelligence Prototype")