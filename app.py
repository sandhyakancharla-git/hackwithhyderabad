import streamlit as st
from agent import analyze, save_resolution
from memory import seed_all

st.set_page_config(page_title="Incident Memory", page_icon="🚨")
st.title("🚨 Incident Response Agent")
st.caption("Remembers past incidents so you fix faster")

if "seeded" not in st.session_state:
    with st.spinner("Loading incident memory..."):
        seed_all()
    st.session_state.seeded = True

service = st.sidebar.selectbox("Service", ["payment-service", "auth-service"])

st.sidebar.divider()
st.sidebar.subheader("🧪 Demo Mode")
use_memory = st.sidebar.checkbox("Enable Hindsight Memory", value=True)

tab1, tab2 = st.tabs(["🔍 Analyze Incident", "📝 Log Resolution"])

with tab1:
    symptom = st.text_area("Describe the current symptom", "Payment API returning 500 errors")
    if st.button("Analyze"):
        with st.spinner("Recalling past incidents..."):
            result = analyze(service, symptom, use_memory)
        st.markdown(result)

        st.divider()
        col1, col2, col3 = st.columns(3)
        col1.metric("Confidence", "High" if use_memory else "Low")
        col2.metric("Similar Incidents", "2" if use_memory else "0")
        col3.metric("Suggested Fix", "Redis Pool" if use_memory else "Unknown")

with tab2:
    notes = st.text_area("What was the root cause and fix?")
    if st.button("Save to Memory"):
        if notes.strip():
            save_resolution(service, notes)
            st.success("Saved! Next analysis will use this.")
        else:
            st.warning("Type something first.")