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

instruction = st.text_input("Enter your prompt:", "How does a mortal man face and defeat the Kraken?")

if st.button('Let\'s Go!'):
  start = time.time()
  response = model.generate_content(instruction)
  end = time.time()
  st.write(response.text)
  st.write("Time to generate: " + str(round(end-start,2)) + " seconds")
