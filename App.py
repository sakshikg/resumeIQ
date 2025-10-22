import streamlit as st
import nltk
import spacy
nltk.download('stopwords')
spacy.load('en_core_web_sm')

import pandas as pd
import base64, random
import time, datetime
from pyresparser import ResumeParser
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter

import io
from streamlit_tags import st_tags
from PIL import Image
import pymysql

# Your custom modules
from Courses import ds_course, web_course, android_course, ios_course, uiux_course, resume_videos, interview_videos

import pafy
import plotly.express as px
import youtube_dl
import re

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""
if "show_signup" not in st.session_state:
    st.session_state.show_signup = False


def is_valid_password(password: str) -> bool:
    """Password must be exactly 8 characters with at least 1 special character"""
    pattern = r'^(?=.*[!@#$%^&*()_+{}\[\]:;"\'<>,.?/~`\\|-])[A-Za-z0-9!@#$%^&*()_+{}\[\]:;"\'<>,.?/~`\\|-]{8}$'
    return bool(re.match(pattern, password))


def load_modern_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    /* Hide Streamlit branding */
    #MainMenu, footer, header {visibility: hidden;}

    /* Main container */
    .login-container {
        background: #fff;
        border-radius: 25px;
        padding: 3rem;
        max-width: 450px;
        width: 100%;
        margin: auto;
        box-shadow: 0 20px 60px rgba(0,0,0,0.25);
        font-family: 'Poppins', sans-serif;
        animation: fadeUp 0.6s ease-out;
    }

    @keyframes fadeUp {
        from {opacity: 0; transform: translateY(30px);}
        to {opacity: 1; transform: translateY(0);}
    }

    /* Header */
    .login-header h1 {
        text-align: center;
        font-size: 2rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 1.5rem;
    }

    /* Tabs */
    .tab-container {
        display: flex;
        justify-content: space-between;
        background: #f7fafc;
        border-radius: 12px;
        padding: 0.4rem;
        margin-bottom: 2rem;
    }

    .tab-button {
        flex: 1;
        padding: 0.8rem;
        font-weight: 600;
        font-size: 1rem;
        border: none;
        background: transparent;
        border-radius: 10px;
        color: #718096;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .tab-button.active {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        color: #fff;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }

    /* Inputs */
    .stTextInput>div>div>input {
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 0.9rem 1.2rem;
        font-size: 1rem;
        background: #f7fafc;
        transition: all 0.3s ease;
    }
    .stTextInput>div>div>input:focus {
        border-color: #6a11cb;
        background: #fff;
        box-shadow: 0 0 0 3px rgba(106,17,203,0.15);
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        color: #fff;
        border: none;
        border-radius: 20px;
        padding: 1rem;
        font-weight: 700;
        font-size: 1rem;
        width: 100%;
        letter-spacing: 0.5px;
        margin-top: 1rem;
        box-shadow: 0 6px 20px rgba(102,126,234,0.3);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102,126,234,0.45);
    }

    /* Links */
    .link-text {
        text-align: center;
        margin-top: 1rem;
        font-size: 0.95rem;
        color: #718096;
    }
    .link-text a {
        color: #6a11cb;
        font-weight: 600;
        text-decoration: none;
        cursor: pointer;
    }
    .link-text a:hover {
        color: #2575fc;
        text-decoration: underline;
    }

    /* Forgot password */
    .forgot-password {
        text-align: right;
        margin-top: 0.5rem;
        margin-bottom: 1rem;
    }
    .forgot-password a {
        color: #6a11cb;
        text-decoration: none;
        font-weight: 500;
        font-size: 0.9rem;
        cursor: pointer;
    }
    .forgot-password a:hover {
        color: #2575fc;
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)


# --- Modern login/signup/reset page ---
def modern_login_page():
    load_modern_css()  # Your existing CSS

    # --- Inline CSS for link-style buttons ---
    st.markdown("""
    <style>
    /* Only style the link-like buttons */
    .stButton>button.link-button {
        background-color: transparent;
        border: none;
        color: #1a73e8;
        text-decoration: underline;
        cursor: pointer;
        padding: 0;
        font-size: 14px;
    }
    .stButton>button.link-button:hover {
        color: #1558b0;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- Session states ---
    if "show_signup" not in st.session_state:
        st.session_state.show_signup = False
    if "show_reset" not in st.session_state:
        st.session_state.show_reset = False
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # --- Main container ---
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)

    # --- Header ---
    if st.session_state.show_reset:
        st.markdown("<div class='login-header'><h1>Reset Password</h1></div>", unsafe_allow_html=True)
    elif st.session_state.show_signup:
        st.markdown("<div class='login-header'><h1>Create Your Account</h1></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='login-header'><h1>Welcome to ResumeIQ</h1></div>", unsafe_allow_html=True)

    # --- Tabs ---
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login", key="login_tab", use_container_width=True):
            st.session_state.show_signup = False
            st.session_state.show_reset = False
    with col2:
        if st.button("Signup", key="signup_tab", use_container_width=True):
            st.session_state.show_signup = True
            st.session_state.show_reset = False

    st.markdown("<hr>", unsafe_allow_html=True)

    # ------------------------------
    # RESET PASSWORD
    # ------------------------------
    if st.session_state.show_reset:
        username_or_email = st.text_input("Username or Email", key="reset_input", placeholder="username or email")
        new_password = st.text_input(
            "New Password (8 chars with special char)", type="password", key="reset_pass", max_chars=8
        )

        if st.button("Reset Password", key="reset_btn", use_container_width=True):
            if not username_or_email or not new_password:
                st.error("All fields are required!")
            elif not is_valid_password(new_password):
                st.error("Password must be 8 chars with a special character!")
            else:
                # Check user table
                cursor.execute("SELECT * FROM user_data WHERE username=%s OR email=%s", (username_or_email, username_or_email))
                user = cursor.fetchone()
                if user:
                    cursor.execute(
                        "UPDATE user_data SET password=%s WHERE username=%s OR email=%s",
                        (new_password, username_or_email, username_or_email)
                    )
                    connection.commit()
                    st.success("Password reset successfully! Please login again.")
                    st.session_state.show_reset = False
                else:
                    # Check admin table
                    cursor.execute("SELECT * FROM admin_data WHERE username=%s OR email=%s", (username_or_email, username_or_email))
                    admin = cursor.fetchone()
                    if admin:
                        cursor.execute(
                            "UPDATE admin_data SET password=%s WHERE username=%s OR email=%s",
                            (new_password, username_or_email, username_or_email)
                        )
                        connection.commit()
                        st.success("Admin password reset successfully! Please login again.")
                        st.session_state.show_reset = False
                    else:
                        st.error("No account found with this username or email!")

        # Back to login button (styled as link)
        if st.button("Back to Login", key="back_to_login", help="Return to login page"):
            st.session_state.show_reset = False

        # Apply link-button style via JavaScript workaround
        st.markdown("""
            <script>
            const btn = window.parent.document.querySelectorAll('button[kind="secondary"]');
            btn.forEach(b => b.classList.add('link-button'));
            </script>
        """, unsafe_allow_html=True)

    # ------------------------------
    # LOGIN
    # ------------------------------
    elif not st.session_state.show_signup:
        role = st.radio("Login as:", ["User", "Admin (HR)"], key="login_role", horizontal=True)
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass", max_chars=8)

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Login", key="login_btn", use_container_width=True):
                if not username or not password:
                    st.error("Enter username and password!")
                elif not is_valid_password(password):
                    st.error("Invalid password format!")
                else:
                    if role == "User":
                        cursor.execute("SELECT * FROM user_data WHERE username=%s AND password=%s", (username, password))
                        user = cursor.fetchone()
                        if user:
                            st.success(f"Welcome back, {username}!")
                            st.session_state.logged_in = True
                            st.session_state.username = username
                            st.session_state.role = "user"
                        else:
                            st.error("Invalid credentials!")
                    else:
                        cursor.execute("SELECT * FROM admin_data WHERE username=%s AND password=%s", (username, password))
                        admin = cursor.fetchone()
                        if admin:
                            st.success(f"Welcome Admin {username}!")
                            st.session_state.logged_in = True
                            st.session_state.username = username
                            st.session_state.role = "admin"
                        else:
                            st.error("Invalid admin credentials!")

        with col2:
            if st.button("Forgot Password?", key="forgot_btn"):
                st.session_state.show_reset = True
                st.session_state.show_signup = False

        # Signup link
        if st.button("Signup now", key="signup_link"):
            st.session_state.show_signup = True
            st.session_state.show_reset = False

    # ------------------------------
    # SIGNUP
    # ------------------------------
    else:
        role = st.radio("Register as:", ["User", "Admin (HR)"], key="register_role", horizontal=True)
        username = st.text_input("Username", key="register_username", max_chars=50)
        email = st.text_input("Email", key="register_email")
        password = st.text_input("Password (8 chars with special char)", type="password", key="register_password", max_chars=8)

        if st.button("Create Account", key="signup_btn", use_container_width=True):
            if not username or not password or not email:
                st.error("All fields are required!")
            elif not is_valid_password(password):
                st.error("Password must be 8 chars with a special character!")
            else:
                if role == "User":
                    cursor.execute("SELECT * FROM user_data WHERE username=%s", (username,))
                    if cursor.fetchone():
                        st.warning("Username already exists!")
                    else:
                        cursor.execute(
                            "INSERT INTO user_data (username, password, email) VALUES (%s, %s, %s)",
                            (username, password, email)
                        )
                        connection.commit()
                        st.success(f"User {username} registered successfully!")
                        st.session_state.role = "user"
                else:
                    cursor.execute("SELECT * FROM admin_data WHERE username=%s", (username,))
                    if cursor.fetchone():
                        st.warning("Admin username already exists!")
                    else:
                        cursor.execute(
                            "INSERT INTO admin_data (username, password, email) VALUES (%s, %s, %s)",
                            (username, password, email)
                        )
                        connection.commit()
                        st.success(f"Admin {username} registered successfully!")
                        st.session_state.role = "admin"

                st.session_state.logged_in = True
                st.session_state.username = username

        # Back to login from signup
        if st.button("Already a member? Login now", key="back_to_login_from_signup"):
            st.session_state.show_signup = False
            st.session_state.show_reset = False

    st.markdown("</div>", unsafe_allow_html=True)


def create_logo():
    """Create ResumeIQ logo"""
    logo_html = """
    <div class="logo-container">
        <svg width="60" height="60" viewBox="0 0 60 60" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="60" height="60" rx="15" fill="url(#gradient)"/>
            <rect x="15" y="18" width="30" height="24" rx="3" fill="white"/>
            <circle cx="23" cy="26" r="3" fill="url(#gradient)"/>
            <rect x="30" y="24" width="8" height="2" rx="1" fill="url(#gradient)"/>
            <rect x="30" y="28" width="10" height="2" rx="1" fill="url(#gradient)"/>
            <rect x="18" y="34" width="15" height="2" rx="1" fill="url(#gradient)"/>
            <rect x="18" y="37" width="10" height="2" rx="1" fill="url(#gradient)"/>
            <defs>
                <linearGradient id="gradient" x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0%" stop-color="#4a90e2"/>
                    <stop offset="100%" stop-color="#e94e8c"/>
                </linearGradient>
            </defs>
        </svg>
        <span class="logo-text">ResumeIQ</span>
    </div>
    """
    st.markdown(logo_html, unsafe_allow_html=True)


def fetch_yt_video(link):
    try:
        video = pafy.new(link)
        return video.title
    except:
        return "Video Title"


def get_table_download_link(df, filename, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}" style="text-decoration:none;"><button style="background: linear-gradient(135deg, #4a90e2, #e94e8c); color: white; border: none; padding: 12px 30px; border-radius: 25px; cursor: pointer; font-weight: 600;">{text}</button></a>'
    return href


def get_excel_download_link(df, filename, text):
    """Generate Excel download link"""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Resume_Analysis')
    processed_data = output.getvalue()
    b64 = base64.b64encode(processed_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}" style="text-decoration:none;"><button style="background: linear-gradient(135deg, #4a90e2, #e94e8c); color: white; border: none; padding: 12px 30px; border-radius: 25px; cursor: pointer; font-weight: 600;">{text}</button></a>'
    return href


def create_individual_report(resume_data, resume_score, reco_field, cand_level, recommended_skills, rec_course):
    """Create individual Excel report for user"""
    report_data = {
        'Field': ['Name', 'Email', 'Phone', 'Resume Score', 'Experience Level', 'Recommended Field', 
                  'Current Skills', 'Recommended Skills', 'Recommended Courses'],
        'Value': [
            resume_data.get('name', 'N/A'),
            resume_data.get('email', 'N/A'), 
            resume_data.get('mobile_number', 'N/A'),
            f"{resume_score}/100",
            cand_level,
            reco_field,
            ', '.join(resume_data.get('skills', [])),
            ', '.join(recommended_skills),
            ', '.join(rec_course) if rec_course else 'N/A'
        ]
    }
    
    df_report = pd.DataFrame(report_data)
    return df_report


def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
    
    converter.close()
    fake_file_handle.close()
    return text


def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" style="border: 3px solid #4a90e2; border-radius: 20px;"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


def course_recommender(course_list):
    st.markdown('<div class="section-header">Recommended Courses for You</div>', unsafe_allow_html=True)
    c = 0
    rec_course = []
    no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 4)
    random.shuffle(course_list)
    
    st.markdown('<div class="info-card blue-card">', unsafe_allow_html=True)
    for c_name, c_link in course_list:
        c += 1
        st.markdown(f"**{c}.** [{c_name}]({c_link})")
        rec_course.append(c_name)
        if c == no_of_reco:
            break
    st.markdown('</div>', unsafe_allow_html=True)
    return rec_course


# Database connection
connection = pymysql.connect(
    host='localhost',
    user='root',                 
    password='Shriyan@25',  
    database='resumeiq',
    port=3306        
)

cursor = connection.cursor()


def insert_data(name, email, res_score, timestamp, no_of_pages, reco_field, cand_level, skills, recommended_skills, courses):

    DB_table_name = 'user_data'

    try:
        insert_sql = f"""
        INSERT INTO {DB_table_name} 
        (id, name, email, resume_score, timestamp, total_pages, recommended_field, candidate_level, actual_skills, recommended_skills, courses)
        VALUES (0, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Make sure all values are strings or correct types
        rec_values = (
            name,
            email,
            float(res_score) if res_score is not None else None,
            timestamp,
            int(no_of_pages) if no_of_pages is not None else None,
            reco_field,
            cand_level,
            skills,
            recommended_skills,
            courses
        )

        cursor.execute(insert_sql, rec_values)
        connection.commit()
        print("Data inserted successfully!")

    except pymysql.DataError as e:
        print(f"Data error: {e}")
    except pymysql.MySQLError as e:
        print(f"MySQL error: {e}")



st.set_page_config(
    page_title="ResumeIQ - Smart Resume Analyser",
    page_icon='🎯',
    layout="wide"
)


def user_page():
    """Single resume analysis for regular users"""
    load_modern_css()
    
    st.markdown("""
    <div class="main-header">
        <h1>Welcome to ResumeIQ</h1>
        <p>AI-Powered Resume Analysis with Smart Career Recommendations</p>
    </div>
    """, unsafe_allow_html=True)
    
    create_logo()
    
    # Logout button in sidebar
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.rerun()
    
    # Database setup
    db_sql = """CREATE DATABASE IF NOT EXISTS SRA;"""
    cursor.execute(db_sql)
    connection.select_db("sra")

    DB_table_name = 'user_data'
    table_sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
                    (ID INT NOT NULL AUTO_INCREMENT,
                     Name varchar(100) NOT NULL,
                     Email_ID VARCHAR(50) NOT NULL,
                     resume_score VARCHAR(8) NOT NULL,
                     Timestamp VARCHAR(50) NOT NULL,
                     Page_no VARCHAR(5) NOT NULL,
                     Predicted_Field VARCHAR(25) NOT NULL,
                     User_level VARCHAR(30) NOT NULL,
                     Actual_skills VARCHAR(300) NOT NULL,
                     Recommended_skills VARCHAR(300) NOT NULL,
                     Recommended_courses VARCHAR(600) NOT NULL,
                     PRIMARY KEY (ID));
                    """
    cursor.execute(table_sql)
    
    st.markdown('<div class="section-header">Upload Your Resume for Analysis</div>', unsafe_allow_html=True)
    pdf_file = st.file_uploader("Choose your Resume (PDF format only)", type=["pdf"])
    
    if pdf_file is not None:
        save_image_path = './Uploaded_Resumes/' + pdf_file.name
        with open(save_image_path, "wb") as f:
            f.write(pdf_file.getbuffer())
        
        st.markdown('<div class="section-header">Resume Preview</div>', unsafe_allow_html=True)
        show_pdf(save_image_path)
        
        # Parse Resume
        resume_data = ResumeParser(save_image_path).get_extracted_data()
        
        if resume_data:
            resume_text = pdf_reader(save_image_path)

            st.markdown('<div class="section-header">Resume Analysis Results</div>', unsafe_allow_html=True)
            
            # Personal Information Section
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown('<div class="info-card pink-card">', unsafe_allow_html=True)
                st.subheader("Personal Information")
                
                if resume_data.get('name'):
                    st.success(f"Hello **{resume_data['name']}**!")
                
                st.markdown('<div class="personal-info-grid">', unsafe_allow_html=True)
                
                if resume_data.get('name'):
                    st.markdown(f"""
                    <div class="info-item">
                        <div class="info-label">Full Name</div>
                        <div class="info-value">{resume_data['name']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                if resume_data.get('email'):
                    st.markdown(f"""
                    <div class="info-item">
                        <div class="info-label">Email Address</div>
                        <div class="info-value">{resume_data['email']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                if resume_data.get('mobile_number'):
                    st.markdown(f"""
                    <div class="info-item">
                        <div class="info-label">Phone Number</div>
                        <div class="info-value">{resume_data['mobile_number']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                if resume_data.get('no_of_pages'):
                    st.markdown(f"""
                    <div class="info-item">
                        <div class="info-label">Resume Pages</div>
                        <div class="info-value">{resume_data['no_of_pages']} page(s)</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Experience Level Assessment
            with col2:
                st.markdown('<div class="info-card blue-card">', unsafe_allow_html=True)
                st.subheader("Experience Level Assessment")
                
                cand_level = ''
                if resume_data['no_of_pages'] == 1:
                    cand_level = "Fresher"
                    st.info("**Fresher Level** - Starting your career journey")
                elif resume_data['no_of_pages'] == 2:
                    cand_level = "Intermediate" 
                    st.success("**Intermediate Level** - Growing professional")
                elif resume_data['no_of_pages'] >= 3:
                    cand_level = "Experienced"
                    st.warning("**Experienced Level** - Seasoned professional")
                
                st.markdown('</div>', unsafe_allow_html=True)

            # Skills Analysis
            st.markdown('<div class="section-header">Skills Analysis & Recommendations</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown('<div class="info-card">', unsafe_allow_html=True)
                st.subheader("Your Current Skills")
                keywords = st_tags(label='Skills extracted from your resume:',
                                   text='These skills were identified in your resume',
                                   value=resume_data['skills'], key='1')
                st.markdown('</div>', unsafe_allow_html=True)

            # Field Recommendation Logic (follows flowchart)
            ds_keyword = ['tensorflow', 'keras', 'pytorch', 'machine learning', 'deep learning', 'flask', 'streamlit']
            web_keyword = ['react', 'django', 'node js', 'react js', 'php', 'laravel', 'magento', 'wordpress', 'javascript', 'angular js', 'c#', 'flask']
            android_keyword = ['android', 'android development', 'flutter', 'kotlin', 'xml', 'kivy']
            ios_keyword = ['ios', 'ios development', 'swift', 'cocoa', 'cocoa touch', 'xcode']
            uiux_keyword = ['ux', 'adobe xd', 'figma', 'zeplin', 'balsamiq', 'ui', 'prototyping', 'wireframes', 'storyframes', 'adobe photoshop', 'photoshop', 'editing', 'adobe illustrator', 'illustrator', 'adobe after effects', 'after effects', 'adobe premier pro', 'premier pro', 'adobe indesign', 'indesign', 'wireframe', 'solid', 'grasp', 'user research', 'user experience']

            recommended_skills = []
            reco_field = ''
            rec_course = []
            field_matched = False

            # Check if skills match known fields
            for i in resume_data['skills']:
                skill_lower = i.lower()
                
                if skill_lower in ds_keyword:
                    field_matched = True
                    reco_field = 'Data Science'
                    st.success("**Career Recommendation:** Data Science roles are perfect for you!")
                    recommended_skills = ['Data Visualization', 'Predictive Analysis', 'Statistical Modeling', 'Data Mining', 'Clustering & Classification', 'Data Analytics', 'Quantitative Analysis', 'Web Scraping', 'ML Algorithms', 'Keras', 'Pytorch', 'Probability', 'Scikit-learn', 'Tensorflow', "Flask", 'Streamlit']
                    with col2:
                        st.markdown('<div class="info-card pink-card">', unsafe_allow_html=True)
                        st.subheader("Recommended Skills to Add")
                        recommended_keywords = st_tags(label='Boost your profile with these skills:', 
                                                       text='Adding these skills will increase your job prospects', 
                                                       value=recommended_skills, key='2')
                        st.markdown('</div>', unsafe_allow_html=True)
                    rec_course = course_recommender(ds_course)
                    break

                elif skill_lower in web_keyword:
                    field_matched = True
                    reco_field = 'Web Development'
                    st.success("**Career Recommendation:** Web Development roles are ideal for you!")
                    recommended_skills = ['React', 'Django', 'Node JS', 'React JS', 'php', 'laravel', 'Magento', 'wordpress', 'Javascript', 'Angular JS', 'c#', 'Flask', 'SDK']
                    with col2:
                        st.markdown('<div class="info-card pink-card">', unsafe_allow_html=True)
                        st.subheader("Recommended Skills to Add")
                        recommended_keywords = st_tags(label='Boost your profile with these skills:', 
                                                       text='Adding these skills will increase your job prospects', 
                                                       value=recommended_skills, key='3')
                        st.markdown('</div>', unsafe_allow_html=True)
                    rec_course = course_recommender(web_course)
                    break

                elif skill_lower in android_keyword:
                    field_matched = True
                    reco_field = 'Android Development'
                    st.success("**Career Recommendation:** Android Development roles are great for you!")
                    recommended_skills = ['Android', 'Android development', 'Flutter', 'Kotlin', 'XML', 'Java', 'Kivy', 'GIT', 'SDK', 'SQLite']
                    with col2:
                        st.markdown('<div class="info-card pink-card">', unsafe_allow_html=True)
                        st.subheader("Recommended Skills to Add")
                        recommended_keywords = st_tags(label='Boost your profile with these skills:', 
                                                       text='Adding these skills will increase your job prospects', 
                                                       value=recommended_skills, key='4')
                        st.markdown('</div>', unsafe_allow_html=True)
                    rec_course = course_recommender(android_course)
                    break

                elif skill_lower in ios_keyword:
                    field_matched = True
                    reco_field = 'IOS Development'
                    st.success("**Career Recommendation:** iOS Development roles are perfect for you!")
                    recommended_skills = ['IOS', 'IOS Development', 'Swift', 'Cocoa', 'Cocoa Touch', 'Xcode', 'Objective-C', 'SQLite', 'Plist', 'StoreKit', "UI-Kit", 'AV Foundation', 'Auto-Layout']
                    with col2:
                        st.markdown('<div class="info-card pink-card">', unsafe_allow_html=True)
                        st.subheader("Recommended Skills to Add")
                        recommended_keywords = st_tags(label='Boost your profile with these skills:', 
                                                       text='Adding these skills will increase your job prospects', 
                                                       value=recommended_skills, key='5')
                        st.markdown('</div>', unsafe_allow_html=True)
                    rec_course = course_recommender(ios_course)
                    break

                elif skill_lower in uiux_keyword:
                    field_matched = True
                    reco_field = 'UI-UX Development'
                    st.success("**Career Recommendation:** UI/UX Design roles are excellent for you!")
                    recommended_skills = ['UI', 'User Experience', 'Adobe XD', 'Figma', 'Zeplin', 'Balsamiq', 'Prototyping', 'Wireframes', 'Storyframes', 'Adobe Photoshop', 'Editing', 'Illustrator', 'After Effects', 'Premier Pro', 'Indesign', 'Wireframe', 'Solid', 'Grasp', 'User Research']
                    with col2:
                        st.markdown('<div class="info-card pink-card">', unsafe_allow_html=True)
                        st.subheader("Recommended Skills to Add")
                        recommended_keywords = st_tags(label='Boost your profile with these skills:', 
                                                       text='Adding these skills will increase your job prospects', 
                                                       value=recommended_skills, key='6')
                        st.markdown('</div>', unsafe_allow_html=True)
                    rec_course = course_recommender(uiux_course)
                    break

            # If no field matched, recommend general skills
            if not field_matched:
                reco_field = 'General Skills'
                st.info("**Career Recommendation:** Consider adding specialized skills to match a specific career field")
                recommended_skills = ['Communication', 'Problem Solving', 'Leadership', 'Teamwork', 'Time Management', 'Critical Thinking']
                with col2:
                    st.markdown('<div class="info-card pink-card">', unsafe_allow_html=True)
                    st.subheader("General Skills to Add")
                    recommended_keywords = st_tags(label='Consider these skills:', 
                                                   text='These general skills are valuable across all fields', 
                                                   value=recommended_skills, key='7')
                    st.markdown('</div>', unsafe_allow_html=True)

            # Resume Quality Scoring (Job Recommendation Engine)
            st.markdown('<div class="section-header">Resume Quality Assessment</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown('<div class="info-card">', unsafe_allow_html=True)
                st.subheader("Scoring Breakdown")
                resume_score = 0
                
                if 'Objective' in resume_text or 'objective' in resume_text:
                    resume_score += 20
                    st.success("**Objective** - Added (20 points)")
                else:
                    st.warning("**Objective** - Missing (0 points) - Add a career objective")

                if 'Declaration' in resume_text or 'declaration' in resume_text:
                    resume_score += 20
                    st.success("**Declaration** - Added (20 points)")
                else:
                    st.warning("**Declaration** - Missing (0 points) - Add a declaration")

                if 'Hobbies' in resume_text or 'Interests' in resume_text or 'hobbies' in resume_text or 'interests' in resume_text:
                    resume_score += 20
                    st.success("**Hobbies/Interests** - Added (20 points)")
                else:
                    st.warning("**Hobbies/Interests** - Missing (0 points) - Show your personality")

                if 'Achievements' in resume_text or 'achievements' in resume_text:
                    resume_score += 20
                    st.success("**Achievements** - Added (20 points)")
                else:
                    st.warning("**Achievements** - Missing (0 points) - Highlight your accomplishments")

                if 'Projects' in resume_text or 'projects' in resume_text:
                    resume_score += 20
                    st.success("**Projects** - Added (20 points)")
                else:
                    st.warning("**Projects** - Missing (0 points) - Showcase practical experience")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-number">{resume_score}</div>', unsafe_allow_html=True)
                st.write("**Out of 100**")
                
                progress_bar = st.progress(0)
                for i in range(resume_score + 1):
                    time.sleep(0.005)
                    progress_bar.progress(i)
                
                if resume_score >= 80:
                    st.success("**Excellent Resume!**")
                elif resume_score >= 60:
                    st.info("**Good - Can Improve**")
                elif resume_score >= 40:
                    st.warning("**Needs Improvement**")
                else:
                    st.error("**Critical - Major Updates Needed**")
                
                st.markdown('</div>', unsafe_allow_html=True)

            # Generate Report
            st.markdown('<div class="section-header">Download Your Analysis Report</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="info-card pink-card">', unsafe_allow_html=True)
                st.subheader("Excel Report")
                
                individual_report = create_individual_report(
                    resume_data, resume_score, reco_field, cand_level, 
                    recommended_skills, rec_course
                )
               # Ensure filename is always a string
            filename = resume_data.get('name') or 'Report'  
            filename = filename.replace(' ', '_')

# File path for CSV
            file_path = f"ResumeIQ_Analysis_{filename}.csv"

# Excel download link
            excel_download = get_excel_download_link(
            individual_report, 
            f"ResumeIQ_Analysis_{filename}.xlsx",  # reuse the safe filenam
            "📊 Download Excel Report"
)



            st.markdown(excel_download, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="info-card blue-card">', unsafe_allow_html=True)
                st.subheader("CSV Report")
                csv_download = get_table_download_link(
                    individual_report,
                    f"ResumeIQ_Analysis_{resume_data.get('name', 'Report').replace(' ', '_')}.csv",
                    "📄 Download CSV Report"
                )
                st.markdown(csv_download, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # Store data in database
            ts = time.time()
            cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            timestamp = str(cur_date + '_' + cur_time)

            insert_data(
                resume_data.get('name', 'Unknown'), 
                resume_data.get('email', 'Unknown'), 
                str(resume_score), 
                timestamp,
                str(resume_data.get('no_of_pages', 1)), 
                reco_field, 
                cand_level, 
                str(resume_data.get('skills', [])),
                str(recommended_skills), 
                str(rec_course)
            )

            # Learning Resources
            st.markdown('<div class="section-header">Learning Resources</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="info-card pink-card">', unsafe_allow_html=True)
                st.subheader("Resume Writing Tips")
                resume_vid = random.choice(resume_videos)
                res_vid_title = fetch_yt_video(resume_vid)
                st.write(f"**{res_vid_title}**")
                st.video(resume_vid)
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="info-card blue-card">', unsafe_allow_html=True)
                st.subheader("Interview Preparation")
                interview_vid = random.choice(interview_videos)
                int_vid_title = fetch_yt_video(interview_vid)
                st.write(f"**{int_vid_title}**")
                st.video(interview_vid)
                st.markdown('</div>', unsafe_allow_html=True)

            connection.commit()
            st.balloons()
        else:
            st.error('Unable to parse resume. Please ensure your PDF is readable and properly formatted.')


def admin_page():
    """Multi-resume analysis dashboard for admins"""
    load_modern_css()
    
    st.markdown("""
    <div class="main-header">
        <h1>ResumeIQ Admin Dashboard</h1>
        <p>Manage User Data & Multi-Resume Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    create_logo()
    
    # Logout button in sidebar
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.rerun()
    
    # ✅ Fetch resume data from database
    query = """
    SELECT id, name, email, resume_score, timestamp,
           total_pages, skills_extracted, experience,
           education, contact, matched_jobs
    FROM resumes
    """
    cursor.execute(query)
    data = cursor.fetchall()
    
    if data:
        st.markdown('<div class="section-header">User Analytics Dashboard</div>', unsafe_allow_html=True)
        
        # ✅ Match with 11 columns
        df = pd.DataFrame(data, columns=[
            'ID', 'Name', 'Email', 'Resume Score', 'Timestamp',
            'Total Pages', 'Skills Extracted', 'Experience',
            'Education', 'Contact', 'Matched Jobs'
        ])
        
        # --- Summary Statistics ---
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-number">{len(df)}</div>', unsafe_allow_html=True)
            st.write("**Total Resumes**")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            avg_score = pd.to_numeric(df['Resume Score'], errors='coerce').mean()
            st.markdown(f'<div class="metric-number">{avg_score:.1f}</div>', unsafe_allow_html=True)
            st.write("**Average Score**")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            top_skill = df['Skills Extracted'].mode().iloc[0] if not df.empty else "N/A"
            st.write(f"**{top_skill}**")
            st.write("**Most Common Skill**")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            experienced_users = len(df[df['Experience'].str.contains("Experienced", case=False, na=False)])
            st.markdown(f'<div class="metric-number">{experienced_users}</div>', unsafe_allow_html=True)
            st.write("**Experienced Users**")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # --- Multi-Resume Analysis Section ---
        st.markdown('<div class="section-header">Multi-Resume Analysis</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.subheader("Upload Multiple Resumes for Batch Analysis")
        
        uploaded_files = st.file_uploader("Choose multiple resume PDFs", type=["pdf"], accept_multiple_files=True)
        
        if uploaded_files:
            if st.button("Analyze All Resumes", use_container_width=True):
                results = []
                progress_bar = st.progress(0)
                
                for idx, pdf_file in enumerate(uploaded_files):
                    save_path = './Uploaded_Resumes/' + pdf_file.name
                    with open(save_path, "wb") as f:
                        f.write(pdf_file.getbuffer())
                    
                    resume_data = ResumeParser(save_path).get_extracted_data()
                    
                    if resume_data:
                        resume_text = pdf_reader(save_path)
                        
                        # Simple resume scoring
                        score = 0
                        if 'Objective' in resume_text or 'objective' in resume_text:
                            score += 20
                        if 'Declaration' in resume_text or 'declaration' in resume_text:
                            score += 20
                        if 'Hobbies' in resume_text or 'Interests' in resume_text:
                            score += 20
                        if 'Achievements' in resume_text or 'achievements' in resume_text:
                            score += 20
                        if 'Projects' in resume_text or 'projects' in resume_text:
                            score += 20
                        
                        # Determine level by pages
                        pages = resume_data.get('no_of_pages', 1)
                        if pages == 1:
                            level = "Fresher"
                        elif pages == 2:
                            level = "Intermediate"
                        else:
                            level = "Experienced"
                        
                        results.append({
                            'Filename': pdf_file.name,
                            'Name': resume_data.get('name', 'Unknown'),
                            'Email': resume_data.get('email', 'N/A'),
                            'Score': score,
                            'Level': level,
                            'Pages': pages,
                            'Skills': ', '.join(resume_data.get('skills', []))[:100]
                        })
                    
                    progress_bar.progress((idx + 1) / len(uploaded_files))
                
                if results:
                    results_df = pd.DataFrame(results)
                    st.success(f"Analyzed {len(results)} resumes successfully!")
                    st.dataframe(results_df, use_container_width=True)
                    
                    # Export options
                    col1, col2 = st.columns(2)
                    with col1:
                        excel_link = get_excel_download_link(results_df, 'Multi_Resume_Analysis.xlsx', '📊 Download Excel')
                        st.markdown(excel_link, unsafe_allow_html=True)
                    with col2:
                        csv_link = get_table_download_link(results_df, 'Multi_Resume_Analysis.csv', '📄 Download CSV')
                        st.markdown(csv_link, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # --- Complete Resume Database Table ---
        st.markdown('<div class="section-header">Complete Resume Database</div>', unsafe_allow_html=True)
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            excel_download = get_excel_download_link(df, 'ResumeIQ_All_Resumes.xlsx', '📊 Download All Resume Data (Excel)')
            st.markdown(excel_download, unsafe_allow_html=True)
        
        with col2:
            csv_download = get_table_download_link(df, 'ResumeIQ_All_Resumes.csv', '📄 Download All Resume Data (CSV)')
            st.markdown(csv_download, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # --- Data Visualizations ---
        st.markdown('<div class="section-header">Data Visualizations</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="info-card pink-card">', unsafe_allow_html=True)
            st.subheader("Top Skills Distribution")
            
            skill_counts = df['Skills Extracted'].value_counts().head(10)
            fig = px.pie(values=skill_counts.values, names=skill_counts.index, 
                        title='Top 10 Skills',
                        color_discrete_sequence=px.colors.sequential.RdBu)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="info-card blue-card">', unsafe_allow_html=True)
            st.subheader("Experience Distribution")
            
            exp_counts = df['Experience'].value_counts()
            fig2 = px.pie(values=exp_counts.values, names=exp_counts.index, 
                         title='Experience Level Distribution',
                         color_discrete_sequence=px.colors.sequential.Blues)
            fig2.update_traces(textposition='inside', textinfo='percent+label')
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Score Distribution
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.subheader("Resume Score Distribution")
        
        df['Resume Score Numeric'] = pd.to_numeric(df['Resume Score'], errors='coerce')
        fig3 = px.histogram(df, x='Resume Score Numeric', 
                           title='Resume Score Distribution', 
                           nbins=20,
                           color_discrete_sequence=['#4a90e2'])
        fig3.update_layout(xaxis_title="Resume Score", yaxis_title="Number of Resumes", height=400)
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        st.info("No resume data available yet. Users need to upload resumes first.")



def run():
    """Main application entry point"""
    
    st.set_page_config(
        page_title="ResumeIQ - Smart Resume Analyser",
        page_icon='🎯',
        layout="wide"
    )
    
    if not st.session_state.get("logged_in"):
        # Create database tables
        cursor.execute("CREATE DATABASE IF NOT EXISTS resumeiq")
        connection.select_db("resumeiq")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(8) NOT NULL,
                email VARCHAR(100) NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(8) NOT NULL,
                email VARCHAR(100) NOT NULL
            )
        """)
        
        connection.commit()
        
        # Show modern login page
        modern_login_page()
    
    else:
        # User is logged in - show the main application
        if st.session_state.role == "user":
            user_page()  # Your existing user_page function
        elif st.session_state.role == "admin":
            admin_page()  # Your existing admin_page function


if __name__ == "__main__":
    run()