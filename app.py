import streamlit as st
import os
import json
from pathlib import Path
import time
import tempfile

# =====================================================================
#                         BASE64 LOGOS (INSERT YOUR OWN)
# =====================================================================
SRM_LOGO_BASE64 = "YOUR_FULL_SRM_LOGO_BASE64_STRING"
STJ_LOGO_BASE64 = "YOUR_FULL_ST_JOSEPH_LOGO_BASE64_STRING"

# =====================================================================
#                         SESSION / CONSTANTS
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

            for g in GRADES:
                (base / g).mkdir(exist_ok=True)
                for s in SUBJECTS:
                    (base / g / s).mkdir(exist_ok=True)

            if METADATA_FILE and not os.path.exists(METADATA_FILE):
                with open(METADATA_FILE, "w") as f:
                    json.dump({}, f)

        except Exception as e:
            st.error(f"Folder creation failed: {e}")


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

    key = f"{grade}/{subject}/{filename}"

    return metadata.get(key, {"description": ""})


# =====================================================================
#                         CUSTOM CSS
# =====================================================================
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
        background: var(--bg);
        color: var(--text);
    }

    .hero-container {
        display:flex;
        justify-content:center;
        flex-wrap:wrap;
        gap:35px;
        margin-top:40px;
        margin-bottom:40px;
    }

    .hero-card {
        background-color: var(--card);
        border: 1px solid var(--border);
        width: 380px;
        border-radius: 22px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 6px 25px rgba(0,0,0,0.35);
        transition: transform 0.25s ease, box-shadow 0.25s ease, border 0.25s ease;
    }

    .hero-card:hover {
        transform: translateY(-8px) scale(1.03);
        box-shadow: 0 10px 35px rgba(0,0,0,0.55);
        border: 1px solid #4c8bf5;
    }

    .app-title {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        -webkit-background-clip:text;
        color:transparent;
        font-size:3rem;
        font-weight:800;
        margin-bottom:10px;
    }
    </style>
    """, unsafe_allow_html=True)


# =====================================================================
#                         NAVIGATION
# =====================================================================
def navigate_to(p):
    st.session_state.page = p


# =====================================================================
#                         HOME PAGE WITH HERO CARDS
# =====================================================================
def home_page():

    st.markdown("""
        <div style="text-align:center; margin-top:20px;">
            <h1 class="app-title">NotesHub</h1>
            <p style="font-size:1.2rem; opacity:0.85;">
                A Community Connect initiative by SRM IST, Ramapuram – IT Department  
                supporting St. Joseph’s Higher Secondary School, Cuddalore
            </p>
        </div>
    """, unsafe_allow_html=True)

    # ============= HERO CARDS =============
    st.markdown(f"""
    <div class="hero-container">

        <!-- SRM Card -->
        <div class="hero-card">
            <img src="data:image/png;base64,{SRM_LOGO_BASE64}" 
                 style="width:150px; border-radius:12px; margin-bottom:15px;">
            <h2 style="color:var(--text); font-size:1.3rem; font-weight:600;">
                SRM IST – Ramapuram (IT Department)
            </h2>
            <p style="opacity:0.85; font-size:0.95rem; line-height:1.5;">
                Developed by second-year IT students under the <b>Community Connect</b> initiative
                to support digital learning infrastructure for schools.
            </p>
        </div>

        <!-- St Joseph's Card -->
        <div class="hero-card">
            <img src="data:image/png;base64,{STJ_LOGO_BASE64}" 
                 style="width:150px; border-radius:12px; margin-bottom:15px;">
            <h2 style="color:var(--text); font-size:1.3rem; font-weight:600;">
                St. Joseph’s HSS – Cuddalore
            </h2>
            <p style="opacity:0.85; font-size:0.95rem; line-height:1.5;">
                Partner institution using NotesHub for centralized study resources 
                for Grade 9–12 students.
            </p>
        </div>

    </div>
    """, unsafe_allow_html=True)

    # ============= FOOTER =============
    st.markdown("""
    <div style="width:100%; text-align:center; margin-top:50px; opacity:0.7;
                font-size:0.9rem; padding:20px 0;">
        Developed by <b>SRM IT Students – Community Connect 2025</b>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.button("Get Started →", on_click=navigate_to, args=("upload",))
    with col2:
        st.button("Browse Notes", on_click=navigate_to, args=("view",))


# =====================================================================
#                         UPLOAD PAGE
# =====================================================================
def upload_page():

    st.title("Upload Study Materials")

    with st.form("upload_form"):
        grade = st.selectbox("Select Grade", GRADES)
        subject = st.selectbox("Select Subject", SUBJECTS)
        file = st.file_uploader("Choose PDF", type="pdf")
        desc = st.text_area("Description", placeholder="Write something about this note...")

        submit = st.form_submit_button("Upload")

        if submit and file is not None:

            if LOCAL_MODE:
                target = Path(UPLOAD_FOLDER) / grade / subject
                target.mkdir(parents=True, exist_ok=True)
                with open(target / file.name, "wb") as f:
                    f.write(file.getbuffer())
            else:
                key = f"{grade}/{subject}/{file.name}"
                st.session_state[f"file_{key}"] = file.getvalue()

            save_metadata(grade, subject, file.name, desc)

            st.success("Uploaded successfully!")
            time.sleep(2)
            navigate_to("home")

    st.button("← Back to Home", on_click=navigate_to, args=("home",))


# =====================================================================
#                         VIEW NOTES PAGE
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
        st.warning("No notes found!")
        return

    st.success(f"Found {len(files)} notes")

    for file in files:
        name = file.name
        info = get_metadata(grade, subject, name)

        with st.expander(f"📄 {name}"):
            st.write(f"**Description:** {info['description']}")

            if LOCAL_MODE:
                with open(Path(UPLOAD_FOLDER) / grade / subject / name, "rb") as f:
                    st.download_button("Download", f, file_name=name)
            else:
                key = f"{grade}/{subject}/{name}"
                blob = st.session_state.get(f"file_{key}")
                st.download_button("Download", blob, file_name=name)

    st.button("← Back to Home", on_click=navigate_to, args=("home",))


# =====================================================================
#                         MAIN ROUTER
# =====================================================================
def main():
    local_css()

    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "upload":
        upload_page()
    elif st.session_state.page == "view":
        view_notes_page()


if __name__ == "__main__":
    main()
