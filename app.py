import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import os
import time

# Retrieve the OpenAI API key from the environment variables
API_KEY = os.environ["GOOGLE_API_KEY"]
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

st.write("Hougang Workshop :sunglasses: Google's Gemini Pro Large Language Model")

Menu_Option = st.selectbox("**Select** analysis:", ('Summarise the key points of the text', 'Identify possible biases in the text', 'Seek views disagreeing with the text', 'Find angles missing from the text', 'Discuss broader significance of the topics', 'Compare the text with historical events', 'Customise your own unique prompt'))
if Menu_Option == "Summarise the key points of the text":
  instruction = "Summarise the key points of the text."
elif Menu_Option == "Identify possible biases in the text":
  instruction = "Identify possible biases in the text."
elif Menu_Option == "Seek views disagreeing with the text":
  instruction = "Offer perspectives that disagree with the text."
elif Menu_Option == "Find angles missing from the text":
  instruction = "Offer perspectives that are missing from the text."
elif Menu_Option == "Discuss broader significance of the topics":
  instruction = "Draft a conclusion that highlights the broader significance of the topics."
elif Menu_Option == "Compare the text with historical events":
  instruction = "Reflect on the text and draw similiarities and differences to historical events in the last century."
elif Menu_Option == "Customise your own unique prompt":
  instruction = st.text_input("Customise your own unique prompt:", "What are the follow up actions?")

uploaded_file = st.file_uploader("**Upload** the PDF document to analyse:", type = "pdf")
raw_text = ""
if uploaded_file is not None:
  doc_reader = PdfReader(uploaded_file)
  for i, page in enumerate(doc_reader.pages):
    text = page.extract_text()
    if text:
      raw_text = raw_text + text + "\n"

if st.button('Let\'s Go!'):
  start = time.time()
  input = instruction + "\n\n" + raw_text
  if raw_text.strip() != '': 
    input = "Read the text below. " + input
  response = model.generate_content(input)
  end = time.time()
  st.write(response.prompt_feedback)
  st.write(response.text)
  st.write("Time to generate: " + str(round(end-start,2)) + " seconds")
