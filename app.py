import streamlit as st
import os
import time
from openai import OpenAI
from pypdf import PdfReader

# Retrieve the OpenAI API key from the environment variables
CLIENT_API_KEY = os.environ['OPENAI_API_KEY']
client = OpenAI(api_key=CLIENT_API_KEY)

st.write("Welcome to **Readhacker**")
st.write("*Your AI-powered reading and ideation assistant*")

# Set the initial temperature, model ID and maximum_tokens
temperature = 0
if st.toggle("Toggle GPT-4 :robot_face: 9x Input, Quality over Speed"):
  maximum_tokens = 120000
  model_id = "gpt-4-turbo-preview"
else:
  maximum_tokens = 13000
  model_id = "gpt-3.5-turbo-0125"

with st.expander("Click to read documentation"):
  st.write("- Productivity app by **Sherwood Analytica**")
  st.write("- Upload a PDF or enter free text as input")
  st.write("- Generate a summary or analysis of input") 
  st.write("- Default GPT-3.5 :computer: up to 10,000 words") 
  st.write("- Toggle GPT-4 :robot_face: up to 90,000 words") 
  st.write("- :red[**Answers may not be suitable or accurate**]")
  st.write("- :blue[**Try reloading webpage to troubleshoot**]")

Option_Input = st.selectbox("How will I receive your input?", ('Upload a pdf','Enter free text'))
Option_Action = st.selectbox("What should I do with your input?", ('Condense into key points', 'Shorten into a summary', 'Identify possible biases', 'Identify disagreeing views', 'Identify missing angles', 'Discuss broader significance', 'Compare with historical events', 'Find black swans and grey rhinos', 'Generate markdown for mindmap', 'Customise your own prompt'))

if Option_Action == "Condense into key points":
  instruction = "Summarize the input into bullet points. Identify the main ideas and key details, and condense them into concise bullet points. Recognize the overall structure of the text and create bullet points that reflect this structure. The output should be presented in a clear and organized way. Do not start with any titles."
elif Option_Action == "Shorten into a summary":
  instruction = "Generate a concise and coherent summary from the input below. Highlight the main ideas and key details. Present your output in a clear and organised way, as one single paragraph only."
elif Option_Action == "Identify possible biases":
  instruction = "Highlight any possible biases in the input."
elif Option_Action == "Identify disagreeing views":
  instruction = "Offer perspectives that disagree with the input."
elif Option_Action == "Identify missing angles":
  instruction = "Offer perspectives that are missing from the input."
elif Option_Action == "Discuss broader significance":
  instruction = "Draft a conclusion that highlights the broader significance of the topics in the input. Present the output in a clear and organised way, as one or more paragraphs."
elif Option_Action == "Compare with historical events":
  instruction = "Reflect on the input and draw similiarities and differences to historical events in the last century. Present the output in a clear and organised way, as one or more paragraphs."
elif Option_Action == "Find black swans and grey rhinos":
  instruction = "Generate black swan and grey rhino scenarios from the input. The scenarios should sound plausible and coherent, draw inspiration from actual historical events, and highlight the impact. As I am familiar with the definition of black swans and grey rhinos, there is no need to explain what they are and you can jump straight into the list of scenarios. Present your output in bullet points under the headings Black Swans and Grey Rhinos."
elif Option_Action == "Generate markdown for mindmap":
  instruction = "Use the input to generate a mindmap in Markdown format. Present your output as follows:\n\n# Root\n\n## Branch 1\n - Branchlet 1a\n - Branchlet 1b\n\n## Branch 2\n - Branchlet 2a\n - Branchlet 2b\n\n(and so on...)"
elif Option_Action == "Customise your own prompt":
  instruction = st.text_input("Customise your own unique prompt:", "What are the follow up actions?")

uploaded_file = st.file_uploader("Upload a PDF to summarise or analyse:", type = "pdf")
raw_text = ""
if uploaded_file is not None:
  doc_reader = PdfReader(uploaded_file)
  for i, page in enumerate(doc_reader.pages):
    text = page.extract_text()
    if text:
      raw_text = raw_text + text + "\n"

  start = time.time()
  input = instruction + "\n\nInput:\n\n" + raw_text
  
  response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125", messages=[
        {"role": "system", "content": "You are my diligent and careful intern. You are able to digest articles and essays, and produce quality summaries and analyses in response to input."},
        {"role": "user", "content": input},
      ],
      temperature=0,
    )
  output_text = response.choices[0].message.content
  end = time.time()

  #st.success('This is a success message!', icon="✅")
  container = st.container(border=True)
  container.write(Option_Action)
  container.write(output_text)
  container.write("Time to generate: " + str(round(end-start,2)) + " seconds")
  container.write(response.usage)
  st.snow()
