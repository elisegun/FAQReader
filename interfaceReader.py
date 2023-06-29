import openai
import os
import PyPDF2
from flask import Flask, request, render_template
from pathlib import Path
from dotenv import load_dotenv

app = Flask(__name__)


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Set up your OpenAI API credentials
openai.api_key = os.environ['OPENAI_KEY']
pdf_text = ""  # Global variable to store the text extracted from the PDF


# Read the PDF file and extract text at the start of the application
def extract_text_from_pdf(file_path):
    pdf_file_path = 'FAQ.pdf'
    with open(pdf_file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        pdf_text = ''
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()
        return pdf_text


# Function to generate responses using OpenAI API
def generate_responses(prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.1
    )
    return response.choices[0].text.strip()



@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        question = request.form['question']

        # Generate responses based on the extracted text and user question
        prompt = "Consider the following text from the PDF" \
                 f"{pdf_text}\n\n" \
                 f"The user question is: \"{question}\"" \
                 "\nIf the question is answered in this FAQ database, provide the answer in natural language. " \
                 "If the question is not answered in this FAQ database, reply that you are not" \
                 "sure and will contact an agent."

        response = generate_responses(prompt)

        return render_template('index.html', question=question, response=response)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    pdf_file_path = 'FAQ.pdf'
    pdf_text = extract_text_from_pdf(pdf_file_path)
    app.run(debug=True)
