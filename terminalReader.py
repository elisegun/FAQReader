import openai
import PyPDF2

# Set up your OpenAI API credentials
openai.api_key = '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'


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
    pdf_file_path = 'FAQ.pdf'
    pdf_text = extract_text_from_pdf(pdf_file_path)

    question = input("Enter your question: ")

    # Generate responses based on the extracted text and user question
    prompt = "Read the following text from the PDF. " \
             "If the question is not answered in this FAQ database rely that you are not sure and will contact an agent." \
             "\n" + pdf_text + question

    response = generate_responses(prompt)
    print("Generated response:")
    print(response)


if __name__ == '__main__':
    main()
