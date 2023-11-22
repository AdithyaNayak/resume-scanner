# resume-scanner
<br>
<b>Overview</b>
<br>
The Resume Scanner is a Python application built using Streamlit for creating and managing resumes for both employers and applicants. Employers can filter through applicant resumes based on various criteria, while applicants can submit their resumes for potential job opportunities.
<br>
<br>
<b>Features</b>
<br>
1. User Authentication
Login Page: Users (Employers and Applicants) can log in with their credentials.
Sign Up: New users can create accounts by providing a username and password.
<br>
2. Employer Dashboard
Resume Filtering: Employers can filter applicant resumes based on criteria such as name, education, domain, skills, and experience.
Display Resumes: Filtered resumes are displayed, providing essential details for employer review.
<br>
3. Applicant Dashboard
Resume Submission: Applicants can submit their resumes by entering details such as name, education, skills, experience, and domain.
Submission Confirmation: Upon successful submission, applicants receive a confirmation message.
<br>
<b>File Structure</b>:
<br>
filename.py: Main Python script containing the application logic.
<br>
employers.txt: File storing employer usernames and hashed passwords.
<br>
applicants.txt: File storing applicant usernames and hashed passwords.
<br>
resume_*.txt: Files containing individual applicant resumes.
<br>
<br>
<b>Dependencies</b>
<br>
Streamlit: Used for building the web-based user interface.
<br>
Hashlib: Utilized for hashing and securing user password
<br>
<br>
<b>Notes</b>
<br>
Security: Passwords are securely stored in hashed form using SHA-256.
<br>
Data Persistence: Resumes and user credentials are stored in text files for simplicity.
<br>
<br>
<b>Contributors</b>
<br>
<i>Adithya Darshan</i>
<br>
<i>Abhilash Vinod</i>
<br>
<i>Abhijit Amar</i>
<br>
<i>Aashish M Kumar</i>
