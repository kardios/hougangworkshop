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

st.set_page_config(page_title="HOUGANG WORKSHOP", page_icon=":sunglasses:",)
st.write("**WORK IN PROGRESS**, your smart reading and ideation assistant")

with st.expander("Click to read documentation"):
  st.write("- Productivity app by **EXPERIMENTAL**")
  st.write("- Upload a PDF or enter free text as input")
  st.write("- Generate a summary or analysis of input") 
  st.write("- GPT-4 Omni - up to 128,000 tokens") 
  st.write("- Claude 3.5 Sonnet - up to 200,000 tokens")
  st.write("- O1 Preview - up to 128,000 tokens (EXPERIMENTAL)")
  st.write("- :red[**Answers may not be suitable or accurate**]")
  st.write("- :blue[**Try reloading webpage to troubleshoot**]")

Model_Option = st.selectbox("What Large Language Model do I use?", ('GPT-4 Omni', 'Claude 3.5 Sonnet', 'Gemini 1.5 Pro', 'o1-preview'))

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
prompt_title_list.append("Customise your own prompt")
prompt_text_list.append("Your task is to do research and generate a short update based on an input topic. Present your answer in one concise and coherent paragraph that includes the main ideas, key details and any notable statistics.")

Prompt_Option = st.selectbox("Which Prompt do I use?", prompt_title_list)
index = prompt_title_list.index(Prompt_Option)

if Prompt_Option == "Customise your own prompt":
  prompt = "You are my smart reading and ideation assistant. You will read the input I provide." + st.text_input("Customise your own unique prompt:", prompt_text_list[index])

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
      input = prompt_text_list[index] + "\n\n" + raw_text

      # Claude 3.5 Sonnet
      start = time.time()
      message = anthropic.messages.create(model = "claude-3-5-sonnet-20240620",
                                                   max_tokens = 4096,
                                                   temperature = 0,
                                                   system= "",
                                                   messages=[{"role": "user", "content": input}])
      output_text1 = message.content[0].text
      end = time.time()
      with st.expander("Claude 3.5 Sonnet"):
        st.write(output_text1)
        st.write("Time to generate: " + str(round(end-start,2)) + " seconds")
        st_copy_to_clipboard(output_text1)
      st.snow()
      
      # Gemini 1.5 Pro
      start = time.time()
      gemini = genai.GenerativeModel("gemini-1.5-pro-exp-0827")
      response = gemini.generate_content(input, safety_settings = safety_settings, generation_config = generation_config)
      output_text2 = response.text
      end = time.time()
      with st.expander("Gemini 1.5 Pro"):
        st.write(output_text2)
        st.write("Time to generate: " + str(round(end-start,2)) + " seconds")
        st_copy_to_clipboard(output_text2)
      st.snow()

      # GPT-4 Omni
      start = time.time()
      response = client.chat.completions.create(model="gpt-4o-2024-08-06", 
                                                messages=[{"role": "system", "content": ""},
                                                          {"role": "user", "content": input}],
                                                          temperature=0)
      output_text3 = response.choices[0].message.content
      end = time.time()
      with st.expander("GPT-4 Omni"):
        st.write(output_text3)
        st.write("Time to generate: " + str(round(end-start,2)) + " seconds")
        st_copy_to_clipboard(output_text3)
      st.snow()

      # O1 Preview
      start = time.time()
      response = client.chat.completions.create(model="o1-preview", 
                                                messages=[{"role": "user", "content": input}])
      output_text4 = response.choices[0].message.content      
      end = time.time()
      with st.expander("O1 Preview"):
        st.write(output_text4)
        st.write("Time to generate: " + str(round(end-start,2)) + " seconds")
        st_copy_to_clipboard(output_text4)
      st.snow()

      # Putting it all together
      total_output_text = "**Claude 3.5 Sonnet**\n\n" + output_text1 + "\n\n**Gemini 1.5 Pro**\n\n" + output_text2 + "\n\n**GPT-4 Omni**\n\n" + output_text3 + "\n\n**O1 Preview**\n\n" + output_text4
      st_copy_to_clipboard(total_output_text)
      
  except:
    st.error(" Error occurred when running model", icon="🚨")
