import streamlit as st
import os
import time
from openai import OpenAI
from langchain_community.document_loaders import UnstructuredURLLoader

# Retrieve the OpenAI API key from the environment variables
CLIENT_API_KEY = os.environ['OPENAI_API_KEY']
client = OpenAI(api_key=CLIENT_API_KEY)

st.write("Hougang Workshop :sunglasses: Prototyping the next Readhacker from my Garage")
link = st.text_input("Enter URL:","https://www.channelnewsasia.com")

if st.button('Let\'s Go!'):
  loader = UnstructuredURLLoader(urls=[link])
  data = loader.load()
  raw_text = data[0].page_content

  start = time.time()
  input = "Generate a concise and coherent summary that captures the main ideas and key details:\n\n" + raw_text
  response = client.chat.completions.create(
    model = "gpt-3.5-turbo-0125", messages=[
      {"role": "system", "content": "You are an expert at summarizing documents with accuracy and precision."},
      {"role": "user", "content": input},
    ],
    temperature=0,
  )
  
  output_text = response.choices[0].message.content
  end = time.time()

  st.write(output_text)
  st.write("Time to generate: " + str(round(end-start,2)) + " seconds")
  st.download_button(':scroll:', output_text)
