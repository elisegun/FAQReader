from flask import Flask, request, render_template
import openai
import PyPDF2

app = Flask(__name__)

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


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/getresponse', methods=['POST'])
def get_response():
    question = request.form['question']

    # Read the PDF file and extract text
    pdf_file_path = 'FAQ.pdf'
    pdf_text = extract_text_from_pdf(pdf_file_path)

    # Generate responses based on the extracted text and user question
    prompt = "Read the following text from the PDF. " \
             "If the question is not answered in this FAQ database rely that you are not sure and will contact an " \
             "agent.\n" + pdf_text + question

    response = generate_responses(prompt)
    print(response)
    return render_template('response.html', response=response)


if __name__ == '__main__':
    app.run(debug=True)
