#app.py
import streamlit as st
from docx import Document
import requests
from bs4 import BeautifulSoup

# Title
st.title("Market Research for Innovation Ideas")

# Form submission
with st.form(key='innovation_form'):
    # Input fields
    problem_statement = st.text_area("Problem Statement (200 words)", help="Describe your problem statement. Address only one problem at once.")
    need_for_innovation = st.text_area("What's the need for this innovation?")
    innovation_name = st.text_input("Name your Innovation/Idea (10 words)")
    innovation_description = st.text_area("Describe your Innovation in Brief. (300 words)")
    supporting_evidence = st.text_area("Support your idea with thorough internet researches & facts")
    references = st.text_area("References (links)", help="Provide URLs separated by newline")
    attachments = st.file_uploader("Attachments", type=["jpg", "png", "pdf"], accept_multiple_files=True)
    expectations = st.text_area("Expectations from the company")

    # Submit button
    submit = st.form_submit_button("Submit")

# When form is submitted
if submit:
    # Langchain agent for processing and rewriting (dummy implementation for demonstration)
    processed_references = references.split('\n')
    for ref in processed_references:
        # For the sake of demonstration, using a simple web scraping technique.
        # In reality, you'd have more sophisticated processing for the references.
        response = requests.get(ref)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string
        st.write(f"Processed title from {ref}: {title}")

    # Generate Word file
    doc = Document()
    doc.add_heading('Market Research Report', level=1)
    doc.add_heading('Problem Statement:', level=2)
    doc.add_paragraph(problem_statement)
    doc.add_heading('Need for Innovation:', level=2)
    doc.add_paragraph(need_for_innovation)
    doc.add_heading('Innovation Name:', level=2)
    doc.add_paragraph(innovation_name)
    doc.add_heading('Innovation Description:', level=2)
    doc.add_paragraph(innovation_description)
    doc.add_heading('Supporting Evidence:', level=2)
    doc.add_paragraph(supporting_evidence)
    doc.add_heading('References:', level=2)
    for ref in processed_references:
        doc.add_paragraph(ref)
    doc.add_heading('Expectations:', level=2)
    doc.add_paragraph(expectations)

    # Save the report
    doc.save("report.docx")

    # Provide download link for the report
    st.markdown("[Download the report](report.docx)")

