# Resume Screener Flask Application
This Flask application leverages the powerful LlamaHub Resume Screener package to analyze and screen resumes efficiently. It's designed to help recruiters and HR professionals streamline the candidate evaluation process by automating the resume screening using advanced AI capabilities.
Take a look at this link: https://llamahub.ai/l/llama_packs-resume_screener 

## Features
* Resume Analysis: Uses LlamaHub's Resume Screener to evaluate resumes against specified criteria.
* PDF Handling: Accepts PDF resumes, extracts text, and processes it for analysis.
* Criteria-Based Screening: Screens candidates based on user-defined job descriptions and criteria.
* User-Friendly Interface: Provides an easy-to-use web interface for uploading resumes and entering job criteria.

## Installation
To set up and run this application, follow these steps:

1. Clone the Repository
```
git clone [URL of Your Repository]
cd [Your Repository Name]
```

2. Create a Virtual Environment (Recommended)
```   
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3. Install Dependencies
```
pip install -r requirements.txt
```
Make sure you have a ```requirements.txt``` file in your repository with all the necessary packages including Flask, PyPDF2, and any other dependencies.

4. Set OpenAI API Key
Set your OpenAI API key as an environment variable:
```
export OPENAI_API_KEY='your_api_key_here'
```
### On Windows use 
```
`set OPENAI_API_KEY=your_api_key_here`
```

5. Run the Application
```
python app.py
```
The application will start running on http://localhost:5000.

## Usage
1. Navigate to the Application
   Open your web browser and go to http://localhost:5000.
2. Upload Resume and Enter Criteria
   Upload the candidate's resume in PDF format and enter the job description and screening criteria.
3. Analyze Resume
   Click the submit button to process and analyze the resume. The results will be displayed on the page.

Happy Learning!!
