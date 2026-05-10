import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
from model_engine import analyze_emotions

# --- CONFIGURATION & IBM BRANDING ---
st.set_page_config(page_title="AuraHealth AI | Powered by IBM Z", page_icon="🧘", layout="centered")

# IBM Blue Palette and Professional Styling
st.markdown("""
    <style>
    /* IBM 8-bar logo blue: #0062ff */
    .stButton>button { 
        background-color: #0062ff; 
        color: white; 
        border-radius: 4px; 
        width: 100%; 
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { 
        background-color: #0043ce; 
        border: none;
    }
    .report-box { 
        padding: 20px; 
        border-radius: 8px; 
        background-color: #f4f4f4; 
        border-left: 8px solid #0062ff; 
    }
    h1, h2, h3 { color: #161616; font-family: 'IBM Plex Sans', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("Project AuraHealth")
    st.success("**Compliance:** UN SDG 3 (Health)")
    st.markdown("---")
    st.write("**Enterprise Architecture:**")
    st.caption("- DistilBERT Transformer Engine")
    st.caption("- IBM Z Pervasive Encryption Ready")
    st.caption("- Zero-Trust Data Policy")

# --- MAIN INTERFACE ---
st.title("AuraHealth AI")
st.write("Professional Mental Health Monitoring for Enterprise Environments.")

user_text = st.text_area("Describe your current emotional state:",
                         placeholder="Example: I feel pressured by the upcoming presentation, but I am confident in my skills.",
                         height=150)

if st.button("RUN NEURAL ANALYSIS"):
    if user_text:
        with st.spinner("Processing through Neural Engine..."):
            predictions = analyze_emotions(user_text)

            # Sort by highest confidence
            top_emotion = predictions[0]['label']
            top_score = predictions[0]['score']

            st.write("### Diagnostic Results")

            # --- 1. CONFIDENCE CHECK (Professionalism) ---
            if top_score < 0.5:
                st.warning(
                    "**Low Confidence Detection:** The AI is uncertain about the emotional nuance. Please describe your feelings in more detail for a better diagnosis.")

            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Primary Emotion", value=top_emotion.capitalize())
            with col2:
                st.metric(label="Confidence Level", value=f"{top_score:.2%}")

            # --- 2. RECOMMENDATIONS ---
            st.markdown(f"<div class='report-box'><strong>AI Recommendation:</strong><br>", unsafe_allow_html=True)
            if top_emotion in ['sadness', 'fear', 'anger']:
                st.write("System detected elevated stress. Recommended: 5-minute focused breathing and hydration.")
            elif top_emotion == 'joy':
                st.write("High mental clarity detected. This is an optimal window for complex analytical tasks.")
            else:
                st.write("Stable baseline. Continue current activity with a scheduled 10-minute break.")
            st.markdown("</div>", unsafe_allow_html=True)

            # --- 3. EXPORT FUNCTION (End-to-End Workflow) ---
            st.write("---")
            report_data = f"AuraHealth Report\nDate: {datetime.now()}\nEmotion: {top_emotion}\nConfidence: {top_score:.2%}\nInput: {user_text}"
            st.download_button(
                label="EXPORT CLINICAL REPORT (TXT)",
                data=report_data,
                file_name=f"AuraHealth_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain"
            )

            # Chart
            df = pd.DataFrame(predictions)
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X('score:Q', title='Confidence Score'),
                y=alt.Y('label:N', sort='-x', title='Emotions'),
                color=alt.value('#0062ff')
            ).properties(height=250)
            st.altair_chart(chart, use_container_width=True)
    else:
        st.error("Input field is empty. Please provide data for analysis.")

st.caption(f"© 2026 AuraHealth | IBM Z x UNSA Hackathon Submission | Version 1.1")