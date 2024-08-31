import streamlit as st
import os
import time
from pyairtable import Api
import requests
import json
from anthropic import Anthropic
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from openai import OpenAI
from pypdf import PdfReader

# Retrieve the API keys from the environment variables

py_airtable_access_key = os.environ['AIRTABLE_ACCESS_KEY']
py_airtable_base_id = os.environ['AIRTABLE_BASE_ID']
py_airtable_table_id = os.environ['AIRTABLE_TABLE_ID'] 

CLIENT_API_KEY = os.environ['OPENAI_API_KEY']
CLAUDE_API_KEY = os.environ["ANTHROPIC_API_KEY"]
GEMINI_API_KEY = os.environ["GOOGLE_API_KEY"]

client = OpenAI(api_key=CLIENT_API_KEY)
anthropic = Anthropic(api_key=CLAUDE_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)

safety_settings = {
  HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
  HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
  HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
  HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

generation_config = genai.GenerationConfig(candidate_count = 1, temperature = 0)

st.set_page_config(page_title="Readhacker Beta", page_icon=":sunglasses:",)
st.write("**Readhacker Beta**, your smart reading and ideation assistant")

with st.expander("Click to read documentation"):
  st.write("- Productivity app by **Sherwood Analytica**")
  st.write("- Upload a PDF or enter free text as input")
  st.write("- Generate a summary or analysis of input") 
  st.write("- GPT-4 Omni - up to 128,000 tokens") 
  st.write("- Claude 3.5 Sonnet - up to 200,000 tokens")
  st.write("- Gemini 1.5 Pro - up to 2 million tokens") 
  st.write("- :red[**Answers may not be suitable or accurate**]")
  st.write("- :blue[**Try reloading webpage to troubleshoot**]")

Model_Option = st.selectbox("What Large Language Model do I use?", ('GPT-4 Omni', 'Claude 3.5 Sonnet', 'Gemini 1.5 Pro'))

Option_Input = st.selectbox("How will I receive your input?", ('Upload a pdf','Enter free text'))

get_url = f'https://api.airtable.com/v0/{py_airtable_base_id}/{py_airtable_table_id}'
headers = {
    'Authorization': f'Bearer {py_airtable_access_key}',
    'Content-Type': 'application/json',
}
params = {
    'sort[0][field]': 'Order',
    'sort[0][direction]': 'asc'
}
response = requests.get(get_url, headers=headers, params=params)
pre_loaded_prompt_data = response.json()

prompt_title_list = []
prompt_text_list = []

for item in pre_loaded_prompt_data['records']:
  prompt_title = item['fields']['Name']
  prompt_text = item['fields']['Notes']
  prompt_title_list.append(prompt_title)
  prompt_text_list.append(prompt_text)

Prompt_Option = st.selectbox("Which Prompt do I use?", prompt_title_list)
index = prompt_title_list.index(Prompt_Option)

if Option_Input == "Upload a pdf":
  uploaded_file = st.file_uploader("Upload a PDF to summarise or analyse:", type = "pdf")
  raw_text = ""
  if uploaded_file is not None:
    try:
      doc_reader = PdfReader(uploaded_file)
      with st.spinner("Extracting from PDF document..."):
        for i, page in enumerate(doc_reader.pages):
          text = page.extract_text()
          if text:
            raw_text = raw_text + text + "\n"
    except:
      st.error(" Error occurred when loading document", icon="🚨")
elif Option_Input == "Enter free text":
  raw_text = ""
  input_text = st.text_area("Enter the text you would like me to summarize or analyse and click **Let\'s Go :rocket:**")
  if st.button("Let\'s Go! :rocket:"):
    raw_text = input_text
    
if raw_text.strip() != "":
  try:
    with st.spinner("Running AI Model...."):
    
      start = time.time()
      
      prompt = prompt_text_list[index] + "\n\n<input_source>\n\n" + raw_text + "\n\n</input_source>\n\n"
      st.write(prompt)
      
      if Model_Option == "Claude 3.5 Sonnet":  
        message = anthropic.messages.create(
          model = "claude-3-5-sonnet-20240620",
          max_tokens = 4096,
          temperature = 0,
          system= "",
          messages=[
            {  
              "role": "user",
              "content": [
                {
                  "type": "text",
                  "text": prompt,
                }
              ]
            }
          ]
        )
        output_text = message.content[0].text
  
      elif Model_Option == "Gemini 1.5 Pro":
        gemini = genai.GenerativeModel("gemini-1.5-pro-exp-0827")
        response = gemini.generate_content(prompt, safety_settings = safety_settings, generation_config = generation_config)
        output_text = response.text

      elif Model_Option == "GPT-4 Omni":
        response = client.chat.completions.create(
          model="gpt-4o", messages=[
            {"role": "system", "content": ""},
            {"role": "user", "content": prompt},
          ],
          temperature = 0,
        )
        output_text = response.choices[0].message.content
        
      end = time.time()

    output_container = st.container(border=True)
    output_container.write(output_text)
    output_container.write("Time to generate: " + str(round(end-start,2)) + " seconds")
    st.download_button(':floppy_disk:', output_text)

  except:
    st.error(" Error occurred when running model", icon="🚨")
  
