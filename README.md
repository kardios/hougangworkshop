# Readhacker

**Readhacker** is your AI-powered reading and ideation assistant, designed to enhance your productivity by summarizing documents, analyzing texts, and generating insights with the power of OpenAI's GPT models.

## Features

- **Multiple GPT Models Support:** Choose between GPT-3.5 and GPT-4 models to balance between quality and speed.
- **Document Upload:** Easily upload PDFs for analysis.
- **Text Input:** Enter text directly into the app for quick insights.
- **Comprehensive Analysis Options:** From summarization to identifying biases and beyond, Readhacker offers a wide range of analysis tools.
- **Custom Prompts:** Tailor the AI's focus to suit your specific needs.

## Getting Started

1. **Toggle GPT Model:** Use the toggle switch at the top to select between GPT-3.5 and GPT-4 models based on your preference for speed or depth of analysis.
2. **Input Selection:** Choose how to provide your input—upload a PDF or enter text directly.
3. **Choose Action:** Select what Readhacker should do with your input, from summarizing to generating markdown summaries and more.
4. **Custom Prompts (Optional):** Customize your own prompt for unique analysis needs.

## Usage Instructions

- Upon selecting your input method and desired action, either upload a PDF or enter your text.
- If choosing to enter text directly, type your content into the provided text area and click **Let's Go! :rocket:** to process.
- The AI will then analyze your input according to your selected options and display the results within the app.

## Installation

To run Readhacker locally, you'll need Python and Streamlit installed. Clone the repository, install dependencies, and start the Streamlit server:

```bash
git clone <repository-url>
cd <repository-path>
pip install -r requirements.txt
streamlit run app.py

**Secrets** Ensure you have an OpenAI API key set in your environment variables as OPENAI_API_KEY to authenticate requests to OpenAI's API.

## Dependencies
- Streamlit
- OpenAI
- PyPDF

## Contributing
- Contributions to Readhacker are welcome! Whether it's feature suggestions, bug reports, or code contributions, please feel free to reach out or submit a pull request.

## License
- Specify your license here or indicate if the project is open-source.
