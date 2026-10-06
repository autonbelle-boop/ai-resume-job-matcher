# AI Resume Job Matcher

An AI-powered web application that compares a resume with a job description and estimates how closely the candidate's skills and experience match the position.

## Demo

![AI Resume Job Matcher](Screenshot%202026-09-30%20164335.png)

## Project Overview

This project uses natural language processing (NLP) and text analysis to compare resume content with a job description.

The application extracts text from **PDF and DOCX resumes**, identifies relevant skills, and calculates an estimated match score using **TF-IDF, cosine similarity, and skill matching**.

## Features

* Upload a resume in PDF or DOCX format
* Paste a job description
* Extract text from uploaded resumes
* Identify matching skills and keywords
* Identify skills and keywords that may be missing
* Calculate an estimated resume-to-job match percentage
* Display results through a Flask web interface

## Technologies Used

* Python
* Flask
* HTML & CSS
* TF-IDF
* Cosine Similarity
* Natural Language Processing (NLP)
* PDF Processing with PyPDF
* DOCX Processing with python-docx

## How It Works

1. The user uploads a resume in PDF or DOCX format.
2. The application extracts the text from the resume.
3. The user enters a job description.
4. The application identifies relevant skills and keywords in both documents.
5. TF-IDF is used to analyze text similarity.
6. Cosine similarity measures how closely the resume and job description match.
7. Skill matching is weighted more heavily in the final score.
8. The application displays the estimated match percentage, matching keywords, and missing keywords.

## Matching Method

The final match score combines two types of analysis:

**Skill Matching — 70%**

The application identifies recognized skills and phrases that appear in both the resume and job description.

**Text Similarity — 30%**

TF-IDF and cosine similarity are used to compare the overall text content.

The final score is an automated estimate and should not be treated as a hiring decision.

## Project Structure

```text
ai-resume-job-matcher/
│
├── app.py
├── .gitignore
└── templates/
    └── index.html
```

## Running the Project

Install the required Python packages:

```bash
pip install flask pypdf python-docx
```

Start the Flask application:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## What I Learned

Through this project, I practiced:

* Python programming
* Flask web development
* Natural language processing
* Text processing
* TF-IDF
* Cosine similarity
* PDF text extraction
* DOCX text extraction
* File uploads
* Keyword and skill matching
* Building a practical AI-assisted application
* Using Git and GitHub to document and showcase a software project

## Portfolio Project

This project was created as part of my AI Software Engineering portfolio to demonstrate practical skills in Python, web development, natural language processing, and software engineering.

**Built by Alesha Auton | 2026**
