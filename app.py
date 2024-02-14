import streamlit as st
import os
import time
from openai import OpenAI
from pypdf import PdfReader

# Retrieve the OpenAI API key from the environment variables
CLIENT_API_KEY = os.environ['OPENAI_API_KEY']
client = OpenAI(api_key=CLIENT_API_KEY)

# Set the initial temperature, model ID and maximum_tokens
temperature = 0
if st.toggle("Use GPT-4 Turbo :robot_face: 9x Input, Quality over Speed"):
  maximum_tokens = 120000
  model_id = "gpt-4-turbo-preview"
else:
  maximum_tokens = 13000
  model_id = "gpt-3.5-turbo-0125"

st.write("Readhacker :sunglasses: AI-Powered Reading and Ideation")

with st.expander("Click to expand documentation"):
    st.write("Readhacker is an *experimental* AI-powered reading and ideation application by **Sherwood Analytica**:")
    st.write("- Access cutting-edge GPT-3.5 and GPT-4 AI models")
    st.write("- Upload PDF document or enter free text as input")
    st.write("- Produce summary or brainstorm with the content") 
    st.write("- GPT-3.5 :computer: up to 10,000 words :computer: prioritise speed") 
    st.write("- GPT-4 :robot_face: quality and input length of 90,000 words") 
    st.write("- Try reloading the webpage to troubleshoot issues")
    st.write("- :red[**Answers may not always be suitable or accurate**]")
    st.write("- :red[**You bear responsibility over how they are used**]")
             
uploaded_file = st.file_uploader("**Upload** the PDF document to analyse:", type = "pdf")
raw_text = ""
if uploaded_file is not None:
  doc_reader = PdfReader(uploaded_file)
  for i, page in enumerate(doc_reader.pages):
    text = page.extract_text()
    if text:
      raw_text = raw_text + text + "\n"

  instruction = "Generate a concise and coherent summary of the text below. Include the main ideas and key details. Present your output in bullet points."
  start = time.time()
  input = instruction + "\n\n" + raw_text
  
  response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125", messages=[
        {"role": "system", "content": "You are a diligent and careful intern. You are able to digest articles and essays, and produce quality analysis."},
        {"role": "user", "content": input},
      ],
      temperature=0,
    )
  output_text = response.choices[0].message.content
  end = time.time()

  st.write(response.usage)
  st.write(output_text)
  st.write("Time to generate: " + str(round(end-start,2)) + " seconds")
  st.download_button(':scroll:', output_text)
