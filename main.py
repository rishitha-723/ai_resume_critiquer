import streamlit as st
import PyPDF2
import io
import os
from langchain_ollama import ChatOllama
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="AI Resume Critiquer",
    page_icon="📄",
    layout = "centered"
)
st.title("AI Resume Critiquer")
st.markdown(
    "Upload your resume in PDF format and get instant feedback on how to improve it!"
)
model = ChatOllama(
    model="llama3.2",
    temperature=0
)
uploaded_file = st.file_uploader(
    "Upload your resume (PDF or TXT)",
    type=["pdf", "txt"]
)
job_role = st.text_input(
    "Enter the job role you are applying for"
)

analyze = st.button("Analyze Resume")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text
def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")
                                    
if analyze and uploaded_file:
    try:
        file_content = extract_text_from_file(uploaded_file)

        if not file_content.strip():
            st.error("The uploaded file is empty. Please upload a valid resume.")
            st.stop()
        prompt = f"""Please analyze this resume and provide constructive feedback. 
        Focus on the following aspects:
        1. Content clarity and impact
        2. Skills presentation
        3. Experience descriptions
        4. Specific improvements for {job_role if job_role else 'general job applications'}
        
        Resume:
        {file_content}
        
        Provide structured feedback.
"""

        with st.spinner("Analyzing resume..."):
            response = model.invoke(
            prompt
        )

        st.markdown(
            "## Analysis and Feedback"
        )

        st.write(response.content)

    except Exception as e:
        st.error(f"Error: {str(e)}")