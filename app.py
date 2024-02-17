import streamlit as st
import os
import time
from openai import OpenAI
from pypdf import PdfReader

# Initialize OpenAI client
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

st.write("**Readhacker**, your AI reading and ideation assistant")

# Toggle for model selection
model_id, maximum_tokens = (
    ("gpt-4-turbo-preview", 120000) if st.toggle("Toggle GPT-4 :robot_face: 9x Input, Quality over Speed")
    else ("gpt-3.5-turbo-0125", 13000)
)

# Documentation Expander
with st.expander("Click to read documentation"):
    docs = [
        "- Productivity app by **Sherwood Analytica**",
        "- Upload a PDF or enter free text as input",
        "- Generate a summary or analysis of input",
        "- Default GPT-3.5 :computer: up to 10,000 words",
        "- Toggle GPT-4 :robot_face: up to 90,000 words",
        "- :red[**Answers may not be suitable or accurate**]",
        "- :blue[**Try reloading webpage to troubleshoot**]"
    ]
    for doc in docs:
        st.write(doc)

Option_Input = st.selectbox("How will I receive your input?", ('Upload a pdf', 'Enter free text'))

# Function to get instructions based on action
def get_instruction(action):
    instructions = {
        "Condense into key points": "Summarize the input into bullet points. Identify the main ideas and key details, and condense them into concise bullet points. Recognize the overall structure of the text and create bullet points that reflect this structure. The output should be presented in a clear and organized way. Do not start with any titles.",
        "Shorten into a summary": "Generate a concise and coherent summary. Highlight the main ideas and key details. Present your output in a clear and organised way, as one single paragraph only.",
        "Identify possible biases": "Highlight any possible biases in the input.",
        "Identify disagreeing views": "Offer perspectives that disagree with the input.",
        "Identify missing angles": "Offer perspectives that are missing from the input.",
        "Discuss broader significance": "Draft a conclusion that highlights the broader significance of the topics in the input. Present the output in a clear and organised way, as one or more paragraphs.",
        "Compare with historical events": "Reflect on the input and draw similiarities and differences to historical events in the last century. Present the output in a clear and organised way, as one or more paragraphs.",
        "Black swans and grey rhinos": "Generate black swan and grey rhino scenarios from the input. The scenarios should sound plausible and coherent, draw inspiration from actual historical events, and highlight the impact. As I am familiar with the definition of black swans and grey rhinos, there is no need to explain what they are and you can jump straight into the list of scenarios. Present your output in bullet points under the headings Black Swans and Grey Rhinos.",
        "Generate markdown summary": "Use the input to generate a mindmap in Markdown format. Present your output as follows:\n\n# (Root)\n\n## (Branch 1)\n - (Branchlet 1a)\n - (Branchlet 1b)\n\n## (Branch 2)\n - (Branchlet 2a)\n - (Branchlet 2b)\n\n(and so on...)",
        "Customise your own prompt": "",
    }
    return "You are my reading assistant. You will read the input I provide." + instructions.get(action)

Option_Action = st.selectbox("What should I do with your input?", ('Condense into key points', 'Shorten into a summary', 'Identify possible biases', 'Identify disagreeing views', 'Identify missing angles', 'Discuss broader significance', 'Compare with historical events', 'Black swans and grey rhinos', 'Generate markdown summary', 'Customise your own prompt'))  # List all options
instruction = get_instruction(Option_Action)

# Custom prompt input
if Option_Action == "Customise your own prompt":
    instruction += st.text_input("Customise your own unique prompt:", "What are the follow up actions?")

# Handle PDF upload and text input
raw_text = ""
if Option_Input == "Upload a pdf":
    uploaded_file = st.file_uploader("Upload a PDF to summarise or analyse:", type="pdf")
    if uploaded_file is not None:
        raw_text = "\n".join([page.extract_text() for page in PdfReader(uploaded_file).pages if page.extract_text()])
elif Option_Input == "Enter free text" and st.button("Let's Go! :rocket:"):
    raw_text = st.text_area("Enter the text you would like me to summarize or analyse:")

if raw_text.strip():
    try:
        start = time.time()
        response = client.chat.completions.create(
            model=model_id, 
            messages=[
                {"role": "system", "content": instruction},
                {"role": "user", "content": f"Below is the input:\n\n{raw_text}"}
            ],
            temperature=0,
        )
        end = time.time()
        output_text = response.choices[0].message.content
        st.write(Option_Action, output_text, f"Time to generate: {round(end-start, 2)} seconds", response.usage)
        st.download_button(':scroll:', output_text)
    except Exception as e:
        st.error(f"The input may not too long: {e}", icon="🚨")
