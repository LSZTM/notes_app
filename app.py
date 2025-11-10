import streamlit as st
import os
import json
from pathlib import Path
import time
import tempfile

# =====================================================================
#                         SESSION & CONSTANTS
# =====================================================================
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'notes_metadata' not in st.session_state:
    st.session_state.notes_metadata = {}

GRADES = ["9", "10", "11", "12"]
SUBJECTS = ["English", "Tamil", "Mathematics", "Physics", "Chemistry", "Computer Science"]

LOCAL_MODE = False

if LOCAL_MODE:
    DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop")
    UPLOAD_FOLDER = os.path.join(DESKTOP_PATH, "NotesApp_Uploads")
    METADATA_FILE = os.path.join(UPLOAD_FOLDER, "notes_metadata.json")
else:
    UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), "NotesApp_Uploads")
    METADATA_FILE = None


# =====================================================================
#                         DIRECTORY SETUP
# =====================================================================
def init_directory_structure():
    if LOCAL_MODE:
        try:
            base = Path(UPLOAD_FOLDER)
            base.mkdir(exist_ok=True)

            for grade in GRADES:
                gp = base / grade
                gp.mkdir(exist_ok=True)
                for subject in SUBJECTS:
                    (gp / subject).mkdir(exist_ok=True)

            if METADATA_FILE and not os.path.exists(METADATA_FILE):
                with open(METADATA_FILE, "w") as f:
                    json.dump({}, f)

        except Exception as e:
            st.error(f"Could not create folders: {e}")


init_directory_structure()


# =====================================================================
#                         METADATA
# =====================================================================
def save_metadata(grade, subject, filename, description):
    if LOCAL_MODE and METADATA_FILE:
        try:
            metadata = json.load(open(METADATA_FILE))
        except:
            metadata = {}
    else:
        metadata = st.session_state.notes_metadata

    key = f"{grade}/{subject}/{filename}"

    metadata[key] = {
        "description": description,
        "content": None if LOCAL_MODE else st.session_state.get(f"file_{key}", None)
    }

    if LOCAL_MODE:
        json.dump(metadata, open(METADATA_FILE, "w"))
    else:
        st.session_state.notes_metadata = metadata


def get_metadata(grade, subject, filename):
    if LOCAL_MODE and METADATA_FILE:
        try:
            metadata = json.load(open(METADATA_FILE))
        except:
            metadata = {}
    else:
        metadata = st.session_state.notes_metadata

    return metadata.get(f"{grade}/{subject}/{filename}", {"description": ""})


# =====================================================================
#                         CUSTOM CSS (ORIGINAL + Hero Fix)
# =====================================================================
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
    }

    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.4);
        transition: 0.3s ease;
    }

    /* Hero Card Hover */
    .hero-card:hover {
        transform: translateY(-8px) scale(1.03);
        border: 1px solid #4c8bf5 !important;
        box-shadow: 0 12px 45px rgba(76, 139, 245, 0.45);
    }

    .app-title {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        -webkit-background-clip:text;
        color:transparent;
        font-weight:800;
    }
    </style>
    """, unsafe_allow_html=True)


# =====================================================================
#                         NAVIGATION
# =====================================================================
def navigate_to(page):
    st.session_state.page = page


# =====================================================================
#                         HOME PAGE (Hero Fixed)
# =====================================================================
def home_page():

    # Header
    st.markdown("""
        <div style='text-align:center;'>
            <h1 class='app-title'>NotesHub</h1>
            <p style='font-size:1.2rem; opacity:0.8;'>
                A Community Connect initiative by SRM IST, Ramapuram – IT Department  
                supporting St. Joseph’s Higher Secondary School, Cuddalore
            </p>
        </div>
    """, unsafe_allow_html=True)

    # -------- HERO CARDS (FIXED) --------
    st.markdown(
        """
        <div style='display:flex; justify-content:center; flex-wrap:wrap; gap:30px; margin-top:40px; margin-bottom:40px;'>

            <div class='hero-card' style='background-color:var(--card); border:1px solid var(--border); border-radius:20px; width:380px; padding:25px; text-align:center; transition:0.3s; box-shadow:0 6px 25px rgba(0,0,0,0.35);'>
                <h2 style='margin-bottom:10px; color:var(--text);'>SRM IST – Ramapuram</h2>
                <p style='opacity:0.85; font-size:0.95rem; line-height:1.5;'>
                    The Department of Information Technology at SRM IST, Ramapuram engages in 
                    community outreach through the <b>Community Connect</b> initiative. Students 
                    develop digital solutions that support schools and promote accessible learning.
                </p>
            </div>

            <div class='hero-card' style='background-color:var(--card); border:1px solid var(--border); border-radius:20px; width:380px; padding:25px; text-align:center; transition:0.3s; box-shadow:0 6px 25px rgba(0,0,0,0.35);'>
                <h2 style='margin-bottom:10px; color:var(--text);'>St. Joseph’s HSS – Cuddalore</h2>
                <p style='opacity:0.85; font-size:0.95rem; line-height:1.5;'>
                    St. Joseph’s Higher Secondary School, Cuddalore collaborates in this initiative 
                    to enhance student access to structured study resources for Grades 9–12.
                </p>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # -------- ORIGINAL ABOUT CARD --------
    st.markdown("""
        <div class="card">
            <h3>📚 About NotesHub</h3>
            <p>NotesHub is a simple yet powerful application designed to help students and educators share
            study materials effortlessly. Upload your notes in PDF format and access them anytime, anywhere.</p>
        </div>
    """, unsafe_allow_html=True)

    # -------- ORIGINAL FEATURES --------
    st.header("✨ Your Awesome Features ✨")

    st.subheader("📤 Easy Upload")
    st.write("Upload your study materials in PDF format with just a few clicks.")
    st.write("---")

    st.subheader("📂 Organized Library")
    st.write("All your notes are stored neatly and categorized by grade and subject.")
    st.write("---")

    st.subheader("🌓 Dark/Light Mode")
    st.write("Choose the theme you prefer for comfortable study time.")
    st.write("---")

    col1, col2 = st.columns(2)
    with col1:
        st.button("Get Started →", on_click=navigate_to, args=("upload",))
    with col2:
        st.button("Browse Notes", on_click=navigate_to, args=("view",))

    # -------- FOOTER --------
    st.markdown("""
    <div style='text-align:center; margin-top:50px; opacity:0.7;'>
        Developed by <b>SRM IT Students – Community Connect 2025</b>
    </div>
    """, unsafe_allow_html=True)


# =====================================================================
#                         UPLOAD PAGE (Unmodified)
# =====================================================================
def upload_page():

    st.title("Upload Study Materials")

    with st.form("upload_form"):
        grade = st.selectbox("Select Grade", GRADES)
        subject = st.selectbox("Select Subject", SUBJECTS)
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        description = st.text_area("Note Description")

        submitted = st.form_submit_button("Upload Note")

        if submitted and uploaded_file is not None:

            if LOCAL_MODE:
                folder = Path(UPLOAD_FOLDER) / grade / subject
                folder.mkdir(parents=True, exist_ok=True)
                with open(folder / uploaded_file.name, "wb") as f:
                    f.write(uploaded_file.getbuffer())
            else:
                key = f"{grade}/{subject}/{uploaded_file.name}"
                st.session_state[f"file_{key}"] = uploaded_file.getvalue()

            save_metadata(grade, subject, uploaded_file.name, description)

            st.success(f"Uploaded to Grade {grade} – {subject}")
            time.sleep(2)
            navigate_to("home")

    st.button("Back", on_click=navigate_to, args=("home",))


# =====================================================================
#                         VIEW PAGE (Unmodified)
# =====================================================================
def view_notes_page():

    st.title("Available Study Materials")

    grade = st.selectbox("Select Grade", GRADES)
    subject = st.selectbox("Select Subject", SUBJECTS)

    files = []

    if LOCAL_MODE:
        folder = Path(UPLOAD_FOLDER) / grade / subject
        if folder.exists():
            files = list(folder.glob("*.pdf"))
    else:
        for key in st.session_state.notes_metadata:
            if key.startswith(f"{grade}/{subject}/"):
                files.append(Path(key.split("/")[-1]))

    if not files:
        st.warning("No notes found")
        return

    st.success(f"Found {len(files)} notes")

    for f in files:
        name = f.name
        info = get_metadata(grade, subject, name)

        with st.expander(f"📄 {name}"):
            st.write(f"**Description:** {info['description']}")

            if LOCAL_MODE:
                with open(Path(UPLOAD_FOLDER) / grade / subject / name, "rb") as pdf:
                    st.download_button("Download", pdf, name)
            else:
                file_key = f"{grade}/{subject}/{name}"
                blob = st.session_state.get(f"file_{file_key}")
                st.download_button("Download", data=blob, file_name=name)

    st.button("Back", on_click=navigate_to, args=("home",))


# =====================================================================
#                         MAIN
# =====================================================================
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
