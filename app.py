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
from st_copy_to_clipboard import st_copy_to_clipboard

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

#################
# CHECKING PROMPT
checking_prompt = """You are an expert at verifying whether summaries are consistent with their source text. Your task is to check four summaries against the given input source text and rank them from best to worst based on their accuracy, completeness, and consistency with the input source text.

First, carefully read the input source text contained within the <input_source> tags.

Now, examine the following four summaries contained within the <answer_1>, <answer_2>, <answer_3> and <answer_4> tags.

For each summary, perform the following steps:
1. Analyze the accuracy of the information presented.
2. Check for any factual errors or misrepresentations.
3. Evaluate the completeness of the summary in capturing key points from the source text.
4. Assess the consistency of the summary's tone and perspective with the original text.

After analyzing all four summaries, compare them to determine their relative quality. Rank the summaries from best to worst based on your analysis.

Provide your response in the following format:

**ANALYSIS**
[Provide a detailed analysis of each summary, discussing its strengths and weaknesses in terms of accuracy, completeness, and consistency with the source text.]

**RANKING**
1. [Best summary number]
2. [Second-best summary number]
3. [Third-best summary number]
4. [Worst summary number]

**JUSTIFICATION**
[Explain your ranking, highlighting the key factors that influenced your decision for each summary's placement.

Remember to base your analysis and ranking solely on the information provided in the input source text and the given summaries. Do not introduce any external information or make assumptions beyond what is explicitly stated in the provided content."""

# CHECKING PROMPT
#################

checking_prompt = """You are tasked with evaluating and ranking four different answers produced by Large Language Models (LLMs) based on a given prompt and source text. Your goal is to determine which answer is the most accurate, complete, and consistent with both the prompt and the source text.

First, carefully read the following source text contained within the <input_source> tags.

Now, consider the prompt that was used to generate the answers, contained within the <prompt_text> tags.

The four answers produced by different LLMs are contained within the <answer_1>, <answer_2>, <answer_3> and <answer_4> tags.

To evaluate and rank these answers, follow these steps:

1. Carefully read each answer and compare it to the source text and prompt.
2. Assess each answer based on the following criteria:
   a. Accuracy: How well does the answer align with the information provided in the source text?
   b. Completeness: Does the answer address all aspects of the prompt?
   c. Consistency: Is the answer consistent with both the prompt and the source text?
3. Take notes on the strengths and weaknesses of each answer.
4. Rank the answers from best (1) to worst (4) based on your assessment.

Provide your evaluation and ranking in the following format:

**ASSESSMENT**
[Your assessment of Answer 1, including strengths and weaknesses]
[Your assessment of Answer 2, including strengths and weaknesses]
[Your assessment of Answer 3, including strengths and weaknesses]
[Your assessment of Answer 4, including strengths and weaknesses]

**RANKING**
1. [Best answer number]
2. [Second-best answer number]
3. [Third-best answer number]
4. [Worst answer number]

**JUSTIFICATION**
[Provide a brief explanation for your ranking, highlighting key differences between the answers and why you ranked them in this order]

Remember to be objective and thorough in your assessment, focusing on the content and quality of each answer rather than stylistic differences. Your evaluation should help identify which LLM produced the most effective response to the given prompt based on the provided source text."""
###########

st.set_page_config(page_title="HOUGANG WORKSHOP", page_icon=":sunglasses:",)
st.write("**EXPERIMENT, EVALUATE & EXCITE**, your AI reading and ideation assistant")

with st.expander("Click to read documentation"):
  st.write("- Productivity app by **EXPERIMENTAL**")
  st.write("- Upload a PDF or enter free text as input")
  st.write("- Generate a summary or analysis of input") 
  st.write("- GPT-4 Omni - up to 128,000 tokens") 
  st.write("- Claude 3.5 Sonnet - up to 200,000 tokens")
  st.write("- Strawberry - up to 128,000 tokens (EXPERIMENTAL)")
  st.write("- :red[**Answers may not be suitable or accurate**]")
  st.write("- :blue[**Try reloading webpage to troubleshoot**]")

Model_Option = st.selectbox("DISABLED: What Large Language Model do I use?", ('GPT-4 Omni', 'Claude 3.5 Sonnet', 'Gemini 1.5 Pro', 'Strawberry'))

strawberry_model = st.selectbox("ENABLED: Which o1 series model do I use?", ("o1-mini","o1-preview"))

Option_Input = st.selectbox("ENABLED: How will I receive your input?", ('Upload a pdf','Enter free text'))

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
else:
  prompt = prompt_text_list[index]

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
    with st.spinner("Running AI Model..."):
      input = prompt + "\n\n" + raw_text

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
      gemini = genai.GenerativeModel("gemini-1.5-pro-002")
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
      
      # Strawberry
      start = time.time()
      response = client.chat.completions.create(model=strawberry_model, 
                                                messages=[{"role": "user", "content": input}])
      output_text4 = response.choices[0].message.content      
      end = time.time()
      with st.expander("Strawberry"):
        st.write(output_text4)
        st.write("Time to generate: " + str(round(end-start,2)) + " seconds")
        st_copy_to_clipboard(output_text4)
      st.snow()

      # Putting it all together
      # total_output_text = "**Claude 3.5 Sonnet**\n\n" + output_text1 + "\n\n**Gemini 1.5 Pro**\n\n" + output_text2 + "\n\n**GPT-4 Omni**\n\n" + output_text3 + "\n\n**Strawberry**\n\n" + output_text4
      # st_copy_to_clipboard(total_output_text)

      output_text1 = "  \n\n<answer_1>" + output_text1 + "</answer_1>  \n\n"
      output_text2 = "  \n\n<answer_2>" + output_text2 + "</answer_2>  \n\n"
      output_text3 = "  \n\n<answer_3>" + output_text3 + "</answer_3>  \n\n"
      output_text4 = "  \n\n<answer_4>" + output_text4 + "</answer_4>  \n\n"
      input_text = "  \n\n<input_source>" + raw_text + "</input_source>  \n\n"
      prompt_text = "  \n\n<prompt_text>" + prompt + "</prompt_text>  \n\n"
      input = checking_prompt + input_text + prompt_text + output_text1 + output_text2 + output_text3 + output_text4
      
      # EVALUATION: Use Gemini 1.5 Pro
      start = time.time()
      gemini = genai.GenerativeModel("gemini-1.5-pro-exp-0827")
      response = gemini.generate_content(input, safety_settings = safety_settings, generation_config = generation_config)
      evaluation_text = response.text
      end = time.time()
      with st.expander("EVALUATION"):
        st.write(evaluation_text)
        st.write("Time to generate: " + str(round(end-start,2)) + " seconds")
        st_copy_to_clipboard(evaluation_text)
      st.balloons()

  except:
    st.error(" Error occurred when running model", icon="🚨")
