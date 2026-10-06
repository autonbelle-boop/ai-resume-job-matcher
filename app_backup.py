from flask import Flask, render_template, request
from pypdf import PdfReader
from docx import Document
from collections import Counter
import math
import os
import re


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


STOP_WORDS = {
    "the", "and", "for", "with", "that", "this", "from",
    "are", "you", "your", "our", "will", "have", "has",
    "was", "were", "been", "being", "their", "they",
    "about", "into", "than", "then", "them", "those",
    "these", "also", "can", "may", "not", "but", "all",
    "any", "job", "work", "working", "role", "position",
    "required", "requirements", "including", "using",
    "responsible", "ability", "able", "preferred"
}


SKILL_PHRASES = [
    "machine operator",
    "quality control",
    "quality assurance",
    "customer service",
    "customer support",
    "data entry",
    "administrative assistant",
    "office administration",
    "microsoft office",
    "microsoft excel",
    "microsoft word",
    "problem solving",
    "troubleshooting",
    "technical support",
    "computer skills",
    "communication skills",
    "time management",
    "project management",
    "teamwork",
    "attention to detail",
    "inventory management",
    "warehouse operations",
    "manufacturing",
    "production",
    "production operator",
    "forklift",
    "safety procedures",
    "lockout tagout",
    "python",
    "flask",
    "javascript",
    "typescript",
    "html",
    "css",
    "sql",
    "git",
    "github",
    "artificial intelligence",
    "machine learning",
    "data analysis",
    "data science",
    "software development",
    "software engineering",
    "web development",
    "api",
    "rest api",
    "pandas",
    "scikit learn"
]


def clean_text(text):
    text = text.lower()

    words = re.findall(
        r"[a-zA-Z][a-zA-Z0-9+#.-]*",
        text
    )

    words = [
        word
        for word in words
        if word not in STOP_WORDS and len(word) > 1
    ]

    return words


def calculate_tf(words):
    counts = Counter(words)

    total_words = len(words)

    if total_words == 0:
        return {}

    return {
        word: count / total_words
        for word, count in counts.items()
    }


def calculate_idf(documents):
    document_count = len(documents)

    vocabulary = set()

    for document in documents:
        vocabulary.update(document)

    idf = {}

    for word in vocabulary:

        documents_containing_word = sum(
            1
            for document in documents
            if word in document
        )

        idf[word] = math.log(
            (document_count + 1)
            / (documents_containing_word + 1)
        ) + 1

    return idf


def create_tfidf_vector(words, idf):
    tf = calculate_tf(words)

    return {
        word: tf[word] * idf.get(word, 0)
        for word in tf
    }


def cosine_similarity(vector_a, vector_b):
    all_words = set(vector_a) | set(vector_b)

    if not all_words:
        return 0

    dot_product = sum(
        vector_a.get(word, 0)
        * vector_b.get(word, 0)
        for word in all_words
    )

    magnitude_a = math.sqrt(
        sum(value ** 2 for value in vector_a.values())
    )

    magnitude_b = math.sqrt(
        sum(value ** 2 for value in vector_b.values())
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0

    return dot_product / (
        magnitude_a * magnitude_b
    )


def find_skill_phrases(text):
    text = text.lower()

    found = []

    for phrase in SKILL_PHRASES:

        if phrase in text:
            found.append(phrase)

    return found


def calculate_match(resume_text, job_description):
    """Calculate resume/job description similarity."""

    resume_skills = set(
        find_skill_phrases(resume_text)
    )

    job_skills = set(
        find_skill_phrases(job_description)
    )

    # Calculate skill match
    if job_skills:

        matching_skills = resume_skills.intersection(
            job_skills
        )

        skill_score = (
            len(matching_skills)
            / len(job_skills)
        ) * 100

    else:

        skill_score = 0

    # Calculate general text similarity
    resume_words = clean_text(resume_text)
    job_words = clean_text(job_description)

    if resume_words and job_words:

        documents = [
            resume_words,
            job_words
        ]

        idf = calculate_idf(documents)

        resume_vector = create_tfidf_vector(
            resume_words,
            idf
        )

        job_vector = create_tfidf_vector(
            job_words,
            idf
        )

        similarity = cosine_similarity(
            resume_vector,
            job_vector
        )

        text_score = similarity * 100

    else:

        text_score = 0

    # Skill matches are weighted more heavily
    final_score = (
        (skill_score * 0.70)
        + (text_score * 0.30)
    )

    return round(
        min(final_score, 100),
        2
    )


def find_matching_keywords(
    resume_text,
    job_description
):

    resume_skills = find_skill_phrases(
        resume_text
    )

    job_skills = find_skill_phrases(
        job_description
    )

    matching = [
        skill
        for skill in job_skills
        if skill in resume_skills
    ]

    resume_words = set(
        clean_text(resume_text)
    )

    job_words = set(
        clean_text(job_description)
    )

    matching_words = resume_words.intersection(
        job_words
    )

    important_words = sorted(
        matching_words,
        key=len,
        reverse=True
    )

    for word in important_words:

        if word not in matching:
            matching.append(word)

    return matching[:20]


def find_missing_keywords(
    resume_text,
    job_description
):

    resume_skills = find_skill_phrases(
        resume_text
    )

    job_skills = find_skill_phrases(
        job_description
    )

    missing = [
        skill
        for skill in job_skills
        if skill not in resume_skills
    ]

    return missing[:20]


def extract_pdf_text(file_path):

    text = ""

    reader = PdfReader(
        file_path
    )

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text + "\n"

    return text


def extract_docx_text(file_path):

    document = Document(
        file_path
    )

    text = ""

    for paragraph in document.paragraphs:

        text += paragraph.text + "\n"

    return text


def extract_resume_text(file_path):

    extension = os.path.splitext(
        file_path
    )[1].lower()

    if extension == ".pdf":

        return extract_pdf_text(
            file_path
        )

    elif extension == ".docx":

        return extract_docx_text(
            file_path
        )

    return ""


@app.route(
    "/",
    methods=["GET", "POST"]
)
def home():

    match_percentage = None

    matching_keywords = []

    missing_keywords = []

    error = None

    if request.method == "POST":

        resume = request.files.get(
            "resume"
        )

        job_description = request.form.get(
            "job_description",
            ""
        ).strip()

        if not resume:

            error = "Please upload a resume."

        elif not job_description:

            error = "Please enter a job description."

        else:

            filename = resume.filename

            if filename == "":

                error = "Please select a resume file."

            else:

                allowed_extensions = [
                    ".pdf",
                    ".docx"
                ]

                extension = os.path.splitext(
                    filename
                )[1].lower()

                if extension not in allowed_extensions:

                    error = (
                        "Please upload a PDF "
                        "or DOCX resume."
                    )

                else:

                    os.makedirs(
                        app.config["UPLOAD_FOLDER"],
                        exist_ok=True
                    )

                    file_path = os.path.join(
                        app.config["UPLOAD_FOLDER"],
                        filename
                    )

                    resume.save(
                        file_path
                    )

                    resume_text = extract_resume_text(
                        file_path
                    )

                    if not resume_text.strip():

                        error = (
                            "Could not extract text "
                            "from the resume."
                        )

                    else:

                        match_percentage = calculate_match(
                            resume_text,
                            job_description
                        )

                        matching_keywords = (
                            find_matching_keywords(
                                resume_text,
                                job_description
                            )
                        )

                        missing_keywords = (
                            find_missing_keywords(
                                resume_text,
                                job_description
                            )
                        )

    return render_template(
        "index.html",
        match_percentage=match_percentage,
        matching_keywords=matching_keywords,
        missing_keywords=missing_keywords,
        error=error
    )


if __name__ == "__main__":

    app.run(
        debug=False
    )