import streamlit as st
import os
import time
from openai import OpenAI
from pypdf import PdfReader

# Retrieve the OpenAI API key from the environment variables
CLIENT_API_KEY = os.environ['OPENAI_API_KEY']
client = OpenAI(api_key=CLIENT_API_KEY)

st.write("**Readhacker** :sunglasses: AI-Powered Reading and Ideation")

# Set the initial temperature, model ID and maximum_tokens
temperature = 0
if st.toggle("Toggle GPT-4 :robot_face: 9x Input, Quality over Speed"):
  maximum_tokens = 120000
  model_id = "gpt-4-turbo-preview"
else:
  maximum_tokens = 13000
  model_id = "gpt-3.5-turbo-0125"

with st.expander("Click to expand documentation"):
  st.write("- A experimental app by **Sherwood Analytica**")
  st.write("- Tap cutting-edge GPT-3.5 and GPT-4 models")
  st.write("- Upload PDF or enter free text as input")
  st.write("- Generate summary or do brainstorming") 
  st.write("- Default GPT-3.5 :computer: up to 10,000 words") 
  st.write("- Toggle GPT-4 :robot_face: up to 90,000 words") 
  st.write("- :blue[**Try reloading webpage to troubleshoot**]")
  st.write("- :red[**Answers may not be suitable or accurate**]")
             
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
