import openai
import PyPDF2
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Set up your OpenAI API credentials
openai.api_key = os.environ['OPENAI_KEY']
pdf_text = ""  # Global variable to store the text extracted from the PDF

# Function to extract text from PDF using PyPDF2
def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text


# Function to generate responses using OpenAI API
def generate_responses(prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.1
    )
    return response.choices[0].text.strip()


# Main program
def main():
    # Read the PDF file and extract text
    pdf_file_path = 'FAQ-complete.pdf'
    pdf_text = extract_text_from_pdf(pdf_file_path)

    question = input("Enter your question: ")

    # Generate responses based on the extracted text and user question
    prompt = "This is a FAQ database in table format for insurance with questions and answers. Consider the following " \
             "text from the PDF" \
             f"{pdf_text}\n\n" \
             f"The user question is: \"{question}\"" \
             "If the question is answered in this FAQ database, provide the answer in natural language. " \
             "If the question is not answered in this FAQ database, reply that you are not" \
             "sure and will contact an agent."

    response = generate_responses(prompt)
    print("Generated response:")
    print(response)


if __name__ == '__main__':
    main()
