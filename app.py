import streamlit as st
import os
import telebot
import io
import time
from openai import OpenAI
from pypdf import PdfReader

recipient_user_id = os.environ['RECIPIENT_USER_ID']
bot_token = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(bot_token)

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
st.set_page_config(page_title="Readhacker", page_icon=":sunglasses:",)
st.write("**Readhacker**, your AI reading and ideation assistant")

file = open('text.txt','r')
content = file.read()
file.close()
st.write(content)

maximum_tokens = 120000
model_id = "gpt-4o"
#model_id = "gpt-4-turbo"

st.write("Uses", model_id)

with st.expander("Click to read documentation"):
  st.write("- Productivity app by **Sherwood Analytica**")
  st.write("- Upload a PDF or enter free text as input")
  st.write("- Generate a summary or analysis of input") 
  st.write("- Uses GPT-4-Turbo :robot_face: up to 90,000 words") 
  st.write("- :red[**Answers may not be suitable or accurate**]")
  st.write("- :blue[**Try reloading webpage to troubleshoot**]")

Option_Input = st.selectbox("How will I receive your input?", ('Upload a pdf','Enter free text'))

Option_Action = st.selectbox("What should I do with your input?", ('Shorten into a summary', 'Condense into key points', 'Identify possible biases', 'Identify disagreeing views', 'Identify missing angles', 'Create alternative mental models', 'Discuss broader significance', 'Compare with historical events', 'Black swans and grey rhinos', 'Generate markdown summary', 'Customise your own prompt'))
if Option_Action == "Shorten into a summary":
  instruction = "You are my reading assistant. You will read the input I provide. Generate a concise and coherent summary. Identify the main ideas and key details. Present your output in a clear and organised way, as one single paragraph only."
elif Option_Action == "Condense into key points":
  instruction = "You are my reading assistant. You will read the input I provide. Summarize the input into bullet points. Identify the main ideas and key details, and condense them into concise bullet points. Recognize the overall structure of the text and create bullet points that reflect this structure. The output should be presented in a clear and organized way. Do not start with any titles."
elif Option_Action == "Identify possible biases":
  instruction = "You are my reading assistant. You will read the input I provide. Highlight any possible biases in the input in a clear and organised way, as one or more paragraphs."
elif Option_Action == "Identify disagreeing views":
  instruction = "You are my reading assistant. You will read the input I provide. Offer perspectives that disagree with the input in a clear and organised way, as one or more paragraphs."
elif Option_Action == "Identify missing angles":
  instruction = "You are my reading assistant. You will read the input I provide. Offer perspectives that are missing from the input in a clear and organised way, as one or more paragraphs."
elif Option_Action == "Create alternative mental models":
  instruction = "You are my reading assistant. You will read the input I provide. Generate three alternative mental models to consider the topics in the input in a clear and organised way."
elif Option_Action == "Discuss broader significance":
  instruction = "You are my reading assistant. You will read the input I provide. Draft a conclusion that highlights the broader significance of the topics in the input. Present the output in a clear and organised way, as one or more paragraphs."
elif Option_Action == "Compare with historical events":
  instruction = "You are my reading assistant. You will read the input I provide. Reflect on the input and draw similiarities and differences to historical events in the last century. Present the output in a clear and organised way, as one or more paragraphs."
elif Option_Action == "Black swans and grey rhinos":
  instruction = "You are my reading assistant. You will read the input I provide. Generate black swan and grey rhino scenarios from the input. The scenarios should sound plausible and coherent, draw inspiration from actual historical events, and highlight the impact. As I am familiar with the definition of black swans and grey rhinos, there is no need to explain what they are and you can jump straight into the list of scenarios. Present your output in bullet points under the headings Black Swans and Grey Rhinos."
elif Option_Action == "Generate markdown summary":
  instruction = "You are my reading assistant. You will read the input I provide. Use the input to generate a mindmap in Markdown format. Present your output as follows:\n\n# (Root)\n\n## (Branch 1)\n - (Branchlet 1a)\n - (Branchlet 1b)\n\n## (Branch 2)\n - (Branchlet 2a)\n - (Branchlet 2b)\n\n(and so on...)"
elif Option_Action == "Customise your own prompt":
  instruction = "You are my reading assistant. You will read the input I provide." + st.text_input("Customise your own unique prompt:", "What are the follow up actions?")

if Option_Input == "Upload a pdf":
  uploaded_file = st.file_uploader("Upload a PDF to summarise or analyse:", type = "pdf")
  raw_text = ""
  if uploaded_file is not None:
    doc_reader = PdfReader(uploaded_file)
    for i, page in enumerate(doc_reader.pages):
      text = page.extract_text()
      if text:
        raw_text = raw_text + text + "\n"
elif Option_Input == "Enter free text":
  raw_text = ""
  input_text = st.text_area("Enter the text you would like me to summarize or analyse and click **Let\'s Go :rocket:**")
  if st.button("Let\'s Go! :rocket:"):
    raw_text = input_text

if raw_text.strip() != "":
  try:
    with st.spinner("Running AI model for text generation..."):
      start = time.time()
      input = "Below is the input:\n\n" + raw_text
      response = client.chat.completions.create(
        model=model_id, messages=[
          {"role": "system", "content": instruction},
          {"role": "user", "content": input},
        ],
        temperature=0,
      )
      end = time.time()
    output_text = response.choices[0].message.content
    container = st.container(border=True)
    container.write(Option_Action)
    container.write(output_text)
    container.write("Time to generate: " + str(round(end-start,2)) + " seconds")
    container.write(response.usage)
    st.download_button(':floppy_disk:', output_text)
    if st.button(':fax:'):
      bot.send_message(chat_id=recipient_user_id, text=output_text)
    if st.button(':speech_balloon:'):
      with st.spinner("Running AI model for audio generation..."):
        start = time.time()
        tts_response = client.audio.speech.create(
          model = "tts-1-hd",
          voice = "alloy",
          input = output_text,
        )
        end = time.time()
        st.write("Time to generate: " + str(round(end-start,2)) + " seconds")
        st.audio(tts_response.content, format="audio/mpeg")
  except:
    st.error(" Input length may be too long.", icon="🚨")
