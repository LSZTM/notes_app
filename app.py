import streamlit as st
import os
import json
from pathlib import Path
import time
import tempfile

# ============================================
# SESSION STATE INITIALIZATION
# ============================================
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'notes_metadata' not in st.session_state:
    st.session_state.notes_metadata = {}

# ============================================
# CONSTANTS & SETTINGS
# ============================================
GRADES = ["9", "10", "11", "12"]
SUBJECTS = ["English", "Tamil", "Mathematics", "Physics", "Chemistry", "Computer Science"]

LOCAL_MODE = False  # Set True only when running on desktop
if LOCAL_MODE:
    DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop")
    UPLOAD_FOLDER = os.path.join(DESKTOP_PATH, "NotesApp_Uploads")
    METADATA_FILE = os.path.join(UPLOAD_FOLDER, "notes_metadata.json")
else:
    UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), "NotesApp_Uploads")
    METADATA_FILE = None

# ============================================
# DIRECTORY INITIALIZATION
# ============================================
def init_directory_structure():
    if LOCAL_MODE:
        try:
            base_path = Path(UPLOAD_FOLDER)
            base_path.mkdir(exist_ok=True)
            
            for grade in GRADES:
                grade_path = base_path / grade
                grade_path.mkdir(exist_ok=True)
                
                for subject in SUBJECTS:
                    subject_path = grade_path / subject
                    subject_path.mkdir(exist_ok=True)
            
            if METADATA_FILE and not os.path.exists(METADATA_FILE):
                with open(METADATA_FILE, 'w') as f:
                    json.dump({}, f)
                    
            st.toast(f"Storage folder ready at: {UPLOAD_FOLDER}", icon="✅")
        except Exception as e:
            st.error(f"Could not create folders: {e}")

init_directory_structure()

# ============================================
# METADATA MANAGEMENT
# ============================================
def save_metadata(grade, subject, filename, description):
    if LOCAL_MODE and METADATA_FILE:
        try:
            with open(METADATA_FILE, 'r') as f:
                metadata = json.load(f)
        except:
            metadata = {}
    else:
        metadata = st.session_state.notes_metadata
    
    key = f"{grade}/{subject}/{filename}"
    metadata[key] = {
        "description": description,
        "content": None if LOCAL_MODE else st.session_state.get(f"file_{key}", None)
    }
    
    if LOCAL_MODE and METADATA_FILE:
        with open(METADATA_FILE, 'w') as f:
            json.dump(metadata, f)
    else:
        st.session_state.notes_metadata = metadata


def get_metadata(grade, subject, filename):
    if LOCAL_MODE and METADATA_FILE:
        try:
            with open(METADATA_FILE, 'r') as f:
                metadata = json.load(f)
        except:
            metadata = {}
    else:
        metadata = st.session_state.notes_metadata
    
    key = f"{grade}/{subject}/{filename}"
    return metadata.get(key, {"description": ""})


# ============================================
# CUSTOM CSS
# ============================================
def local_css():
    st.markdown("""
    <style>
    :root {
        --primary: #6C63FF;
        --secondary: #FF6584;
        --bg: #121212;
        --text: #E0E0E0;
        --card: #1E1E1E;
        --border: #2E2E2E;
    }

    .stApp {
        background-color: var(--bg);
        color: var(--text);
    }

    .card {
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        background-color: var(--card);
        border: 1px solid var(--border);
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }

    .hero-container {
        display: flex;
        gap: 25px;
        margin-top: 40px;
        margin-bottom: 40px;
        justify-content: center;
        flex-wrap: wrap;
    }

    .hero-card {
        background-color: var(--card);
        border: 1px solid var(--border);
        width: 420px;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 6px 25px rgba(0,0,0,0.35);
        transition: all 0.3s ease;
    }

    .hero-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.45);
    }

    .hero-logo {
        width: 110px;
        height: auto;
        margin-bottom: 15px;
        border-radius: 12px;
    }

    .hero-title {
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 10px;
        color: var(--text);
    }

    .hero-text {
        font-size: 0.95rem;
        opacity: 0.85;
        margin-bottom: 15px;
        line-height: 1.5;
    }

    .app-title {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        -webkit-background-clip: text;
        color: transparent;
        font-size: 3rem;
        font-weight: 800;
    }
    </style>
    """, unsafe_allow_html=True)


# ============================================
# NAVIGATION CONTROL
# ============================================
def navigate_to(page):
    st.session_state.page = page


# ============================================
# HOME PAGE WITH HERO CARDS
# ============================================
def home_page():
    st.markdown("""
        <div style="text-align:center; margin-top:20px;">
            <h1 class="app-title">NotesHub</h1>
            <p style="font-size: 1.2rem; opacity: 0.85;">
                A Community Connect initiative by SRM IST, Ramapuram – IT Department  
                supporting St. Joseph’s Higher Secondary School, Cuddalore
            </p>
        </div>
        """, unsafe_allow_html=True)

    # HERO CARDS
    st.markdown("""
    <div class="hero-container">

        <div class="hero-card">
            <img src="https://i.imgur.com/9V3K2cY.png" class="hero-logo">
            <div class="hero-title">SRM IST – Ramapuram (IT Department)</div>
            <div class="hero-text">
                Developed by second-year IT students under the Community Connect program.  
                The goal is to enhance digital learning accessibility for students in Tamil Nadu.
            </div>
        </div>

        <div class="hero-card">
            <img src="https://i.imgur.com/5bXo3eJ.png" class="hero-logo">
            <div class="hero-title">St. Joseph’s HSS – Cuddalore</div>
            <div class="hero-text">
                Partner institution benefiting from a centralized digital notes repository  
                designed for Grade 9–12 students across multiple subjects.
            </div>
        </div>

    </div>
    """, unsafe_allow_html=True)

    # ABOUT
    st.markdown("""
        <div class="card">
            <h3>📘 About NotesHub</h3>
            <p>
                NotesHub is a simplified and modern platform for uploading and accessing study materials.
                It bridges the gap between educators and learners, ensuring structured academic support.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.header("✨ Key Features")
    st.subheader("📤 Easy Upload")
    st.write("Upload PDF files seamlessly using a clean interface.")

    st.write("---")
    st.subheader("📂 Organized Library")
    st.write("Notes categorized by grade and subject for easy navigation.")

    st.write("---")
    st.subheader("🌓 Dark/Light Mode")
    st.write("Comfortable reading experience at all times.")

    st.write("---")

    col1, col2 = st.columns(2)
    with col1:
        st.button("Get Started →", on_click=navigate_to, args=("upload",))
    with col2:
        st.button("Browse Notes", on_click=navigate_to, args=("view",))


# ============================================
# UPLOAD PAGE
# ============================================
def upload_page():
    st.title("Upload Study Materials")
    
    with st.form("upload_form"):
        grade = st.selectbox("Select Grade", GRADES)
        subject = st.selectbox("Select Subject", SUBJECTS)
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        description = st.text_area("Note Description", placeholder="Enter a brief description...")

        submitted = st.form_submit_button("Upload Note")

        if submitted and uploaded_file is not None:
            if LOCAL_MODE:
                target_dir = Path(UPLOAD_FOLDER) / grade / subject
                target_dir.mkdir(parents=True, exist_ok=True)
                file_path = target_dir / uploaded_file.name
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
            else:
                file_key = f"{grade}/{subject}/{uploaded_file.name}"
                st.session_state[f"file_{file_key}"] = uploaded_file.getvalue()

            save_metadata(grade, subject, uploaded_file.name, description)

            st.success(f"File uploaded to Grade {grade} - {subject} successfully!")
            time.sleep(2)
            navigate_to("home")

    st.button("Back to Home", on_click=navigate_to, args=("home",))


# ============================================
# VIEW NOTES PAGE
# ============================================
def view_notes_page():
    st.title("Available Study Materials")

    grade = st.selectbox("Select Grade", GRADES)
    subject = st.selectbox("Select Subject", SUBJECTS)

    if LOCAL_MODE:
        target_dir = Path(UPLOAD_FOLDER) / grade / subject
        files = list(target_dir.glob("*.pdf")) if target_dir.exists() else []
    else:
        files = []
        for key in st.session_state.notes_metadata:
            if key.startswith(f"{grade}/{subject}/"):
                filename = key.split("/")[-1]
                files.append(Path(filename))

    if not files:
        st.warning(f"No notes found for Grade {grade} {subject}")
    else:
        st.success(f"Found {len(files)} notes.")
        for file in files:
            filename = file.name

            metadata = get_metadata(grade, subject, filename)

            with st.expander(f"📄 {filename}"):
                st.markdown(f"""
                <div class="card">
                    <h4>{filename}</h4>
                    <p><strong>Description:</strong> {metadata['description']}</p>
                </div>
                """, unsafe_allow_html=True)

                if LOCAL_MODE:
                    with open(UPLOAD_FOLDER, "rb") as f:
                        st.download_button("Download", f, filename)
                else:
                    file_key = f"{grade}/{subject}/{filename}"
                    file_data = st.session_state.get(f"file_{file_key}")
                    st.download_button("Download", data=file_data, file_name=filename, mime="application/pdf")

    st.button("Back to Home", on_click=navigate_to, args=("home",))


# ============================================
# MAIN APPLICATION ROUTER
# ============================================
def main():
    local_css()

    if st.session_state.page == 'home':
        home_page()
    elif st.session_state.page == 'upload':
        upload_page()
    elif st.session_state.page == 'view':
        view_notes_page()


if __name__ == "__main__":
    main()
