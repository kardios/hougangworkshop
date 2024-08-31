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

for item in data['records']:
  prompt_title = item['fields']['Name']
  prompt_text = item['fields']['Notes']
  prompt_title_list.append(prompt_title)
  prompt_text_list.append(prompt_text)

Prompt_Option = st.selectbox("Which Prompt do I use?", prompt_title_list)
index = prompt_title_list.index(Prompt_Option)
