import streamlit as st
import os
from datetime import datetime

# -------------------- CONFIG --------------------
st.set_page_config(page_title="📘 CSBS Notes Archive", layout="wide")

# Folder to store uploaded notes
UPLOAD_DIR = "notes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -------------------- SESSION STATE --------------------
if "username" not in st.session_state:
    st.session_state.username = None
if "role" not in st.session_state:
    st.session_state.role = None

# -------------------- USERS --------------------
users = {
    "avadhijain2004": {"password": "Aryhi@0204", "role": "teacher"},
    "student": {"password": "student123", "role": "student"}  # Example student login
}

# -------------------- Login Panel --------------------
with st.sidebar:
    st.title("🔐 Login")

    if st.session_state.username:
        st.success(f"Logged in as {st.session_state.username} ({st.session_state.role})")
        if st.button("Logout"):
            st.session_state.username = None
            st.session_state.role = None
    else:
        uname = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.button("Login"):
            if uname in users and users[uname]["password"] == pwd:
                st.session_state.username = uname
                st.session_state.role = users[uname]["role"]
                st.success("Login successful!")
            else:
                st.error("Invalid credentials")

# -------------------- Title --------------------
st.title("📚 CSBS Notes Archive")
st.write("Welcome! Choose your semester and download the notes you need.")

# -------------------- Semester & Subject Info --------------------
csbs_subjects = {
    "Semester 1": ["Discrete Mathematics", "Statistics and Probability", "Fundamentals of Computer Science", "Business Communication and Value Science I","Principles of Electrical Engineering","Physics for Computing Science"],
    "Semester 2": ["Linear Algebra", "Statistical Methods", "Data Structures and Algorithms", "Business Communication and Value Science II","Fundamentals of Ecomonics", "Principles of Electronics Engineering"],
    "Semester 3": ["Computational Statistics", "Software Engineering", "Computer Organization and Architecture","Formal Logic and Automata Theory","Financial Management","Object Oriented Programming"],
    "Semester 4": ["DBMS", "Operating System", "Business Communication and Value Science III","Software Design with UML","Marketing Management","Innovation and Entrepreneurship","Operations Research"],
    "Semester 5": ["Compiler Design", "Machine Learning", "Analysis and Design of Algorithms","Fundamentals of Management","Industrial Psychology","Business Strategy","Design Thinking","Mini Project"],
    "Semester 6": ["Modern Web Applications", "Artificial Intelligence", "Financial Cost Accounting","Image Processing and Pattern Recognition","Business Communication and Value Science IV","Information Security","Computer Networks"],
    "Semester 7": ["Mobile Computing", "UDSA","MATLAB","IoT","SSSM","ITPM","HRM"],
    "Semester 8": ["Internship"]
}

selected_sem = st.selectbox("🎓 Select Semester", list(csbs_subjects.keys()))
selected_subject = st.selectbox("📘 Select Subject", csbs_subjects[selected_sem])

# -------------------- Upload Notes --------------------
if st.session_state.role == "teacher":
    st.subheader("📤 Upload Notes")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    if uploaded_file:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{selected_sem}__{selected_subject}__{timestamp}__{uploaded_file.name}"
        save_path = os.path.join(UPLOAD_DIR, filename)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("Note uploaded successfully!")

# -------------------- View Notes --------------------
st.subheader("📂 Available Notes")

files = os.listdir(UPLOAD_DIR)
filtered = [f for f in files if f.startswith(f"{selected_sem}__{selected_subject}")]

if not filtered:
    st.info("No notes uploaded yet for this subject.")
else:
    for file in sorted(filtered, reverse=True):
        _, _, _, filename = file.split("__", 3)
        file_path = os.path.join(UPLOAD_DIR, file)
        with open(file_path, "rb") as f:
            file_bytes = f.read()
        with st.expander(f"📘 {filename}"):
            st.download_button("⬇️ Download", data=file_bytes, file_name=filename, mime="application/pdf")
