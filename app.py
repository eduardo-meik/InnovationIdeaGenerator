# app.py
import streamlit as st
from docx import Document
import requests
from bs4 import BeautifulSoup
import base64
from agent.prompts import *
from agent.llm_utils import choose_agent, create_chat_completion

# Title
st.title("Market Research for Innovation Ideas")

# Helper functions for downloading
def make_downloadable_link(file_path, file_name, download_name):
    with open(file_path, "rb") as f:
        bytes_data = f.read()
        b64 = base64.b64encode(bytes_data).decode()
        return f'<a href="data:application/octet-stream;base64,{b64}" download="{download_name}">{file_name}</a>'

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

    # For now, we'll create a prompt using problem_statement, but you can choose to create more intricate prompts combining multiple fields.
    task = f"Generate a report on the problem statement: '{problem_statement}' considering the innovation named '{innovation_name}' and its relevance: '{innovation_description}'."
    agent_data = choose_agent(task)
    st.write(f"Chosen Agent: {agent_data['agent']}")
    agent_prompt = agent_data["agent_role_prompt"]
    st.write("Generating your report...")
    messages = [
        {"role": "system", "content": agent_prompt},
        {"role": "user", "content": task}
    ]
    report = create_chat_completion(messages=messages, model="gpt-4.0-turbo")  # Assuming a model is specified here

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
    doc.add_paragraph(report)  # Assuming the report is in a format suitable for direct inclusion

    # Save the report
    doc.save("report.docx")

    # Generate a downloadable link and provide it
    download_link = make_downloadable_link("report.docx", "Download the report", "report.docx")
    st.markdown(download_link, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

