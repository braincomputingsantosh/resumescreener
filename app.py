from flask import Flask, request, render_template, send_from_directory, render_template_string
import PyPDF2
import os
import datetime
import uuid
from llama_index.llama_pack import download_llama_pack
from llama_index import ServiceContext


os.environ["OPENAI_API_KEY"] = ""

ResumeScreenerPack = download_llama_pack(
    "ResumeScreenerPack", "./resume_screener_pack"
)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    user_text = request.form.get('text')
    criteria = request.form.get('text')
    file = request.files.get('file')
    extracted_text = ""
    unique_filename = str(uuid.uuid4())
    pdfFile = ""
    extractedTextFile = ""

    if file and allowed_file(file.filename):
        extracted_text = extract_text_from_pdf(file)
        pdfFile = save_file(file, unique_filename, '.pdf')  # Save the PDF file
        print(pdfFile)
        extractedTextFile = save_text_to_file(extracted_text, unique_filename)
        print(extractedTextFile)

    if not user_text and not extracted_text:
        return 'No text entered and no PDF file provided'

    # service_context = ServiceContext.from_defaults(chunk_size=1024, llm=llm, embed_model="local")
    resume_screener = ResumeScreenerPack(
    job_description=user_text,
    criteria=[
        criteria
        ],
    )

    response = resume_screener.run(resume_path=pdfFile)

    criteria = ""
    for cd in response.criteria_decisions:
        criteria += "### CRITERIA DECISION\n"
        criteria += cd.reasoning + "\n"
        # criteria += str(cd.decision) + "\n"
        # Color coding for each decision
        decision_color = "#008000" if cd.decision else "#FF0000"
        criteria += "<span style='color: " + decision_color + ";'><b>" + str(cd.decision) + "</b></span>\n"
        
    criteria += "#### OVERALL REASONING #####\n"
    criteria += str(response.overall_reasoning) + "\n"
    # criteria += str(response.overall_decision)

    # Check the overall_decision and apply color
    decision_color = "#008000" if response.overall_decision else "#FF0000"
    criteria += "<span style='color: " + decision_color + ";'></br>Overall Decision: <b>" + str(response.overall_decision) + "</b></span>"

    return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Extracted Text</title>
            <link rel="stylesheet" href="/static/style.css">
            <style>
                .scrollable-textbox {
                    max-height: 300px; /* Adjust the height as needed */
                    overflow-x: auto; /* Enable horizontal scrolling */
                    overflow-y: auto; /* Enable vertical scrolling */
                    border: 1px solid #ccc;
                    padding: 10px;
                    margin-bottom: 20px;
                    word-wrap: break-word; /* Ensure long words are broken and wrapped to the next line */
                }
                .scrollable-textbox pre {
                    white-space: pre-wrap; /* Allow long lines to wrap in <pre> */
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Requirements:</h1>
                <p>{{ user_text }}</p>
                <div class="scrollable-textbox">
                    <pre>{{ criteria|safe }}</pre>
                </div>
                <h1>Extracted Text from PDF Resume:</h1>
                <div class="scrollable-textbox">
                    <p>{{ extracted_text }}</p>
                </div>
                <a href="/">Back</a>
            </div>
        </body>
        </html>
    """, user_text=user_text, criteria=criteria, extracted_text=extracted_text)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'pdf'}

def extract_text_from_pdf(file):
    # Load PDF file from the Flask file storage
    pdfReader = PyPDF2.PdfReader(file)
    text = ""
    for pageNum in range(len(pdfReader.pages)):
        page = pdfReader.pages[pageNum]
        text += page.extract_text()
    return text

def save_text_to_file(text, unique_filename):
    # Save the extracted text to a .txt file
    text_filename = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename+ '.txt')
    with open(text_filename, 'w', encoding='utf-8') as text_file:
        text_file.write(text)
    return text_filename

def save_file(file, unique_filename, file_extension):
    file_filename = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename + file_extension)
    file.stream.seek(0)  # Reset file stream position to the beginning
    file.save(file_filename)
    return file_filename

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
