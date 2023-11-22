import os
import streamlit as st
import hashlib

USER_FILE_EMPLOYER = "employers.txt"
USER_FILE_APPLICANT = "applicants.txt"


class Resume:
    def __init__(self, name, education, skills, domain, experience):
        self.name = name
        self.education = education
        self.skills = [skill.strip() for skill in skills.split(',')]
        self.domain = domain
        self.experience = int(experience)
        
class ApplicantResume:
    def __init__(self, name, education, skills, experience, domain):
        self.name = name
        self.education = education
        self.skills = [skill.strip() for skill in skills.split(',')]
        self.experience = int(experience)
        self.domain = domain

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

def read_applicant_resumes(file_path):
    resumes = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 5):
            name = lines[i].strip().split(': ')[1]
            education = lines[i + 1].strip().split(': ')[1]
            skills = lines[i + 2].strip().split(': ')[1]
            experience = lines[i + 3].strip().split(': ')[1]
            domain = lines[i + 4].strip().split(': ')[1]
            resumes.append(ApplicantResume(name, education, skills, experience, domain))
    return resumes

def write_applicant_resume(name, education, skills, experience, domain):
    file_name = f"resume_{name.lower().replace(' ', '_')}.txt"
    with open(file_name, 'w') as file:
        file.write(f"Name: {name}\n")
        file.write(f"Education: {education}\n")
        file.write(f"Skills: {skills}\n")
        file.write(f"Experience: {experience}\n")
        file.write(f"Domain: {domain}\n")
    return file_name

def applicant_resume_page():
    st.title("Applicant Resume Page")
    st.subheader("Enter Your Resume Details")

    name = st.text_input("Full Name:")
    education = st.text_input("Education:")
    skills = st.text_input("Skills (comma-separated):")
    experience = st.text_input("Experience (in years):")
    domain = st.text_input("Domain:")

    if st.button("Submit Resume"):
        if name and education and skills and experience and domain:
            write_applicant_resume(name, education, skills, experience, domain)
            st.success("Resume submitted successfully!")
        else:
            st.warning("Please fill in all the fields.")

def write_user(username, password, user_type):

    if user_type == 'employer':
        user_file = USER_FILE_EMPLOYER
    elif user_type == 'applicant':
        user_file = USER_FILE_APPLICANT
    else:
        raise ValueError("Invalid user type")

    with open(user_file, 'a') as file:
        file.write(f"{username}:{hashlib.sha256(password.encode()).hexdigest()}\n")

def check_user_credentials(username, password, user_type):
    if user_type == 'employer':
        user_file = USER_FILE_EMPLOYER
    elif user_type == 'applicant':
        user_file = USER_FILE_APPLICANT
    else:
        raise ValueError("Invalid user type")

    with open(user_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            stored_username, stored_password = line.strip().split(':')
            if username == stored_username and hashlib.sha256(password.encode()).hexdigest() == stored_password:
                return True
    return False

def login_page():
    st.title("Login Page")
    user_type = st.radio("Select User Type:", ('Employer', 'Applicant'))

    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")

    if st.button("Login"):
        if check_user_credentials(username, password, user_type.lower()):
            st.success("Login Successful!")
            st.session_state.user_logged_in = True
            st.session_state.user_type = user_type.lower()
            st.session_state.username = username  
            st.experimental_rerun()
        else:
            st.error("Invalid credentials. Please try again.")

    st.subheader(f"Don't have an account? Sign up below.")

    new_username = st.text_input("New Username:")
    new_password = st.text_input("New Password:", type="password")

    if st.button("Sign Up"):
        if new_username and new_password:
            write_user(new_username, new_password, user_type.lower())
            st.success("Account created successfully! You can now log in.")
        else:
            st.warning("Please provide a username and password for sign up.")

def main():
    if 'user_logged_in' not in st.session_state:
        st.session_state.user_logged_in = False

    if not st.session_state.user_logged_in:
        login_page()  # Show login page by default
        return

    if st.session_state.user_type == 'employer':
        st.title("Resume Filter")
        
        # Display the resume filter here
        resume_files = get_resume_files()

        if not resume_files:
            st.warning("No resume files found in the current directory.")
            return

        resumes = []
        for file in resume_files:
            resumes.extend(read_resumes(file))

        st.sidebar.title("Filters")

        filters = {}
        filter_types = ['name', 'education', 'domain', 'skills', 'experience']
        for filter_type in filter_types:
            if filter_type == 'experience':
                filter_value = st.sidebar.number_input(f"Minimum {filter_type.capitalize()} required:", min_value=0)
            else:
                filter_value = st.sidebar.text_input(f"{filter_type.capitalize()} to filter by:")
            if filter_value:
                filters[filter_type] = filter_value

        filtered_resumes = filter_resumes(resumes, filters)

        st.subheader("Filtered Resumes:")
        for resume in filtered_resumes:
            st.write(f"**Name:** {resume.name}\n"
                     f"**Education:** {resume.education}\n"
                     f"**Skills:** {', '.join(resume.skills)}\n"
                     f"**Domain:** {resume.domain}\n"
                     f"**Experience:** {resume.experience} years\n"
                     f"---")

    elif st.session_state.user_type == 'applicant':
        applicant_resume_page()

if __name__ == "__main__":
    main()



