import os
import streamlit as st

class Resume:
    def __init__(self, name, education, skills, domain, experience):
        self.name = name
        self.education = education
        self.skills = [skill.strip() for skill in skills.split(',')]
        self.domain = domain
        self.experience = int(experience)

def read_resumes(file_path):
    resumes = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 6):
            name = lines[i].strip().split(': ')[1]
            education = lines[i + 1].strip().split(': ')[1]
            skills = lines[i + 2].strip().split(': ')[1]
            domain = lines[i + 3].strip().split(': ')[1]
            experience = lines[i + 4].strip().split(': ')[1]
            resumes.append(Resume(name, education, skills, domain, experience))
    return resumes

def get_resume_files():
    resume_files = [file for file in os.listdir() if file.startswith('resume') and file.endswith('.txt')]
    return resume_files

def filter_resumes(resumes, filters):
    filtered_resumes = resumes
    for key, value in filters.items():
        if key == 'experience':
            filtered_resumes = [resume for resume in filtered_resumes if getattr(resume, key) >= value]
        elif key == 'skills':
            filtered_resumes = [resume for resume in filtered_resumes if value.lower() in [skill.lower() for skill in resume.skills]]
        else:
            filtered_resumes = [resume for resume in filtered_resumes if getattr(resume, key) == value]
    return filtered_resumes

def main():
    st.title("Resume Filter App")

    filters = {}
    filter_labels = ['Name', 'Education', 'Skills', 'Domain', 'Experience']
    for label in filter_labels:
        filters[label.lower()] = st.text_input(label, "")

    filter_button = st.button("Filter Resumes")
    if filter_button:
        resumes = read_and_filter_resumes(filters)
        display_results(resumes)

def read_and_filter_resumes(filters):
    resume_files = get_resume_files()

    if not resume_files:
        return []

    resumes = []
    for file in resume_files:
        resumes.extend(read_resumes(file))

    filtered_resumes = filter_resumes(resumes, filters)
    return filtered_resumes

def display_results(resumes):
    st.subheader("Filtered Resumes:")
    for resume in resumes:
        st.write(f"\nName: {resume.name}\nEducation: {resume.education}\nSkills: {', '.join(resume.skills)}\n"
                 f"Domain: {resume.domain}\nExperience: {resume.experience} years\n\n")

if __name__ == "__main__":
    main()
