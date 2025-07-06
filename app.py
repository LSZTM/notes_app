import streamlit as st
import os
import json
from pathlib import Path
import time
import tempfile

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'notes_metadata' not in st.session_state:
    st.session_state.notes_metadata = {}

# Constants
GRADES = ["9", "10", "11", "12"]
SUBJECTS = ["English", "Tamil", "Mathematics", "Physics", "Chemistry", "Computer Science"]

# For local storage
LOCAL_MODE = False  # Set to False when deploying to Community Cloud
if LOCAL_MODE:
    DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop")
    UPLOAD_FOLDER = os.path.join(DESKTOP_PATH, "NotesApp_Uploads")
    METADATA_FILE = os.path.join(UPLOAD_FOLDER, "notes_metadata.json")
else:
    # For Community Cloud - uses session state and temp files
    UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), "NotesApp_Uploads")
    METADATA_FILE = None

# Create directory structure
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
            
            # Initialize metadata file
            if METADATA_FILE and not os.path.exists(METADATA_FILE):
                with open(METADATA_FILE, 'w') as f:
                    json.dump({}, f)
                    
            st.toast(f"Storage folder ready at: {UPLOAD_FOLDER}", icon="✅")
        except Exception as e:
            st.error(f"Could not create folders: {e}")

# Save note metadata
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

# Get note metadata
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

# Custom CSS
def local_css():
    st.markdown("""
    <style>
    :root {
        --primary: #6C63FF;
        --secondary: #FF6584;
        --bg: #121212;
        --card: #1E1E1E;
        --text: #E0E0E0;
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
        transition: all 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.4);
    }
    
    .stButton>button {
        border: none;
        border-radius: 12px;
        padding: 10px 24px;
        background: linear-gradient(135deg, var(--primary), #8A82FF);
        color: white;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .app-title {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        font-weight: 800;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize directory structure
init_directory_structure()

# Page navigation
def navigate_to(page):
    st.session_state.page = page

# Home Page (unchanged)
def home_page():
    # --- Header Section ---
    st.markdown("""
        <div class="header">
            <h1 class="app-title">NotesHub</h1>
            <p style="font-size: 1.2rem; opacity: 0.8;">Your centralized platform for sharing and accessing study materials</p>
        </div>
        """, unsafe_allow_html=True)

    # --- About NotesHub Card ---
    st.markdown("""
        <div class="card">
            <h3>📚 About NotesHub</h3>
            <p>NotesHub is a simple yet powerful application designed to help students and educators share
            study materials effortlessly. Upload your notes in PDF format and access them anytime, anywhere.</p>
        </div>
        """, unsafe_allow_html=True)

    # --- Features Section ---
    st.header("✨ Your Awesome Features ✨")

    # Feature 1: Easy Upload
    st.subheader("📤 Easy Upload")
    st.write(
        """
        Upload your study materials in PDF format with just a few clicks.
        It's quick, simple, and gets your documents ready in no time!
        """
    )
    st.write("---")

    # Feature 2: Organized Library
    st.subheader("📂 Organized Library")
    st.write(
        """
        All your notes are stored in one place, creating a neat and accessible library.
        Find exactly what you need, precisely when you need it, with ease.
        """
    )
    st.write("---")

    # Feature 3: Dark/Light Mode
    st.subheader("🌓 Dark/Light Mode")
    st.write(
        """
        Choose your preferred theme for comfortable reading at any time.
        Whether you prefer bright and clear or soft and mellow, we've got you covered.
        """
    )
    st.write("---")

    # --- Call to action ---
    col1, col2 = st.columns(2)
    with col1:
        st.button("Get Started →", on_click=navigate_to, args=("upload",), key="home_upload_btn")
    with col2:
        st.button("Browse Notes", on_click=navigate_to, args=("view",), key="home_view_btn")

# Upload Page
def upload_page():
    st.title("Upload Study Materials")
    
    with st.form("upload_form"):
        grade = st.selectbox("Select Grade", GRADES, key="upload_grade")
        subject = st.selectbox("Select Subject", SUBJECTS, key="upload_subject")
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", key="file_uploader")
        description = st.text_area("Note Description", 
                                 placeholder="Enter a brief description of this note...",
                                 key="note_description")
        
        submitted = st.form_submit_button("Upload Note")
        
        if submitted and uploaded_file is not None:
            if LOCAL_MODE:
                # Local storage mode
                target_dir = Path(UPLOAD_FOLDER) / grade / subject
                target_dir.mkdir(parents=True, exist_ok=True)
                file_path = target_dir / uploaded_file.name
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
            else:
                # Community Cloud mode - store in session state
                file_key = f"{grade}/{subject}/{uploaded_file.name}"
                st.session_state[f"file_{file_key}"] = uploaded_file.getvalue()
            
            # Save metadata
            save_metadata(grade, subject, uploaded_file.name, description)
            
            st.success(f"File uploaded successfully to Grade {grade} {subject}!")
            time.sleep(2)
            navigate_to("home")

    st.button("Back to Home", on_click=navigate_to, args=("home",))

# View Notes Page
def view_notes_page():
    st.title("Available Study Materials")
    
    grade = st.selectbox("Select Grade", GRADES, key="view_grade")
    subject = st.selectbox("Select Subject", SUBJECTS, key="view_subject")
    
    if LOCAL_MODE:
        # Local storage mode
        target_dir = Path(UPLOAD_FOLDER) / grade / subject
        files = list(target_dir.glob("*.pdf")) if target_dir.exists() else []
    else:
        # Community Cloud mode - get from session state
        files = []
        for key in st.session_state.notes_metadata:
            if key.startswith(f"{grade}/{subject}/"):
                filename = key.split("/")[-1]
                files.append(Path(filename))
    
    if not files:
        st.warning(f"No notes found for Grade {grade} {subject}")
    else:
        st.success(f"Found {len(files)} notes for Grade {grade} {subject}")
        
        for file in files:
            filename = file.name if isinstance(file, Path) else file
            metadata = get_metadata(grade, subject, filename)
            
            with st.expander(f"📄 {filename}"):
                st.markdown(f"""
                <div class="card">
                    <h4>{filename}</h4>
                    <p><strong>Description:</strong> {metadata['description'] or 'No description available'}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if LOCAL_MODE:
                    with open(file, "rb") as f:
                        st.download_button(
                            label="Download Note",
                            data=f,
                            file_name=filename,
                            mime="application/pdf",
                            key=f"dl_{filename}"
                        )
                else:
                    file_key = f"{grade}/{subject}/{filename}"
                    file_data = st.session_state.get(f"file_{file_key}")
                    if file_data:
                        st.download_button(
                            label="Download Note",
                            data=file_data,
                            file_name=filename,
                            mime="application/pdf",
                            key=f"dl_{filename}"
                        )

    st.button("Back to Home", on_click=navigate_to, args=("home",))

# Main App
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
