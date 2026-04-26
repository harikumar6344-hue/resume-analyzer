import pdfplumber
import re

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
    return text


def clean_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9@.+ ]', '', text)
    return text


def extract_email(text):
    match = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}', text)
    return match[0] if match else None


def extract_phone(text):
    match = re.findall(r'(\+91[\-\s]?)?[6-9]\d{9}', text)
    return match[0] if match else None


skills_list = [
    "python", "sql", "java", "machine learning",
    "excel", "c", "c++", "html", "css", "javascript"
]

def extract_skills(text):
    found_skills = []
    for skill in skills_list:
        if re.search(r'\b' + skill + r'\b', text):
            found_skills.append(skill)
    return found_skills


def extract_name(text):
    words = text.split()
    return " ".join(words[:2]) if len(words) >= 2 else None


def parse_resume(file):
    text = extract_text_from_pdf(file)
    text = clean_text(text)

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text)
        }