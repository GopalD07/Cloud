import streamlit as st
from src.pipeline import run_resume_pipeline

st.set_page_config(page_title="📄 Resume Scanner", layout="wide")

st.title("📄 AI Resume & JD Analyzer")
st.markdown("Upload a resume and job description to get a detailed report: SWOT, ATS score, and improvement tips.")

resume_file = st.file_uploader("📎 Upload Resume", type=["pdf", "docx", "txt"])
jd_file = st.file_uploader("📎 Upload Job Description", type=["pdf", "docx", "txt"])

model_choice = st.selectbox("🔧 Embedding model", ["text-embedding-004"], index=0)

if resume_file and jd_file:
    if st.button("Analyze", type="primary"):
        with st.spinner("Running pipeline..."):
            try:
                report = run_resume_pipeline(resume_file, jd_file, model_name=model_choice)
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.subheader("🧠 SWOT Analysis")
                    st.markdown(report["SWOT_Analysis"])
                with col2:
                    st.subheader("📊 ATS Score")
                    st.markdown(report["ATS_Score"])
                with col3:
                    st.subheader("🔧 Suggestions")
                    st.markdown(report["Suggestions"])
            except Exception as e:
                st.error(f"❌ Error: {e}")
else:
    st.info("⬆️ Please upload both files to begin.")
