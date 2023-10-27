
from flask import Flask, render_template, request, jsonify
import openai
from flask_cors import CORS
import PyPDF2
from PyPDF2 import PdfReader




app = Flask(__name__)
CORS(app)

api_key = ""
openai.api_key = api_key


@app.route('/', methods=['GET'])
def check():
    return jsonify({'gpt_choice': "yes"})

@app.route('/chat', methods=['POST'])
def convert():
    data = request.json
    user_input = data.get("chat")


    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use the chat model
        messages= user_input

        # [
        #     {"role": "system",
        #      "content": ""},
        #     {"role": "user", "content": user_input}]
    )

    gpt_choice = response.choices[0]
    #  gpt_choice = response.choices[len(choices)]

    print(gpt_choice)

    # Return both choices as JSON
    return jsonify({'gpt_choice': gpt_choice})

# ==============================  this method return text from document ===============================

def extract_text_from_pdf(pdf_file):
    try:
        # Create a PdfReader object
        pdf_reader = PdfReader(pdf_file)

        # Initialize a variable to store the text
        text = ''

        # Iterate through each page in the PDF
        for page in pdf_reader.pages:
            text += page.extract_text()

        return text

    except Exception as e:
        return str(e)

# ==========================================================================================


@app.route('/docsummary', methods=['POST'])
def generate_summary():
    print("request recived")

    pdf_file = request.files['pdfFile']
    print("going to convert")
    pdf_text = extract_text_from_pdf(pdf_file)
    print(pdf_text)
    print("converted")

    prompt = f"Summarize the following text:\n\n{pdf_text}\n\n .For summarize use advanced NLP techniques to maintain context and relevance."
    print("calling api")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use the chat model
        messages=[
            {"role": "user", "content": prompt}],
        max_tokens=150,

    )

    print("api called")

    return response


# ==============================================================================================


@app.route('/sentiment', methods=['POST'])
def sentiment():
    data = request.json
    user_input = data.get("chat")


    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use the chat model
        messages=
        [
            {"role": "system",
             "content": "Behave like Sentiment analyzer and Emotion recognizer and only use one word to tell Sentiment and use one word for Emotion. Use appropriate words .Question example= i am happy,  example for result= Sentiment= Positive,Emotion=happy"},
            {"role": "user", "content": user_input}]
    )

    gpt_choice = response.choices[0]
    #  gpt_choice = response.choices[len(choices)]


    print(gpt_choice)

    # Return both choices as JSON
    return jsonify({'gpt_choice': gpt_choice})









if __name__ == '__main__':
  app.run(debug=True,port=8080)

