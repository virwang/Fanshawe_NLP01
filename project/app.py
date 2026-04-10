# app.py
import streamlit as st
from brain import MaintenanceBrain # Import the logic layer

# --- PAGE CONFIGURATION ---
# Using local file 'falcon.png' for the browser tab icon
st.set_page_config(
    page_title="Fanshawe AI Ops Diagnostic Portal", 
    page_icon="falcon.png", 
    layout="centered"
)

# Initialize Brain with caching (singleton pattern)
@st.cache_resource
def load_system():
    return MaintenanceBrain()

try:
    brain = load_system()
except Exception as e:
    st.error(f"Initialization Failed: {e}")
    st.stop()

# --- UI LAYOUT ---
col1, col2 = st.columns([1, 4])
with col1:
    # Use the same local logo for the page header
    st.image("falcon.png", width=80)
with col2:
    st.title("Fanshawe Tech AI Ops")

st.markdown("### Autonomous Maintenance Knowledge Base")
st.divider()

user_input = st.text_input(
    "Describe your technical issue:", 
    placeholder="e.g., File permission issues or server restarts"
)

if user_input:
    with st.spinner('Analyzing expert records...'):
        res = brain.search(user_input)
        
    if res['found']:
        st.subheader("✅ Expert-Verified Solution")

        topic = res.get('topic', 'General Support')
        st.markdown(f"**📍 Question Categorize：** :orange-background[{topic}]")

        st.info(res['answer']) # This will show the polished version from brain.py
        
        #Show confidence score and cluster ID for debugging/insight
        col_meta1, col_meta2 = st.columns(2)
        with col_meta1:
            st.caption(f"🔍 Semantic matching degree: {res['confidence']:.2%}")
        with col_meta2:
            # Debug info: Show cluster ID if available, else show N/A
            # st.caption(f"Cluster ID: {res.get('cluster_id', 'N/A')}")
            pass

        st.success("Issue identified. Follow the steps above.")
        
    else:
        st.error("⚠️ No matching solution found.")
        st.warning("""
            **Fanshawe Tech Support Escalation:** Contact: [support@fanshawetech.com](mailto:support@fanshawetech.com)
        """)

st.divider()
st.caption("© 2026 AI Ops Solutions | Powered by Fanshawe Tech Engine")