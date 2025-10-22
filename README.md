🧠 ResumeIQ — Smart Resume Analyzer

ResumeIQ is an AI-powered resume analysis and career recommendation platform built with Streamlit.
It automatically extracts, analyzes, and evaluates resumes to provide intelligent career guidance, skill enhancement tips, and personalized course recommendations.

Admins (HR) can analyze multiple resumes simultaneously, visualize analytics, and download structured reports.

🚀 Features
👤 User Dashboard

Upload and analyze your resume (PDF format)

Get AI-powered:

Skill extraction and classification

Career field prediction

Resume score (out of 100)

Experience level estimation

Receive personalized:

Recommended skills

Online courses

Learning resources (YouTube integration)

Download detailed Excel and CSV reports

🧑‍💼 Admin Dashboard

Upload and analyze multiple resumes at once

Automatically extract data (skills, score, level, etc.)

Generate and download bulk reports

Visualize:

Top skills distribution

Experience distribution

Resume score distribution

View entire user database in tabular format

🔐 Authentication

Secure login/signup system for both users and admins

Password validation (8 characters with at least one special character)

Password reset feature via UI

🛠️ Tech Stack
Component	Technology
Frontend	Streamlit
Backend	Python
Database	MySQL (via PyMySQL)
AI/Parsing	PyResparser, PDFMiner, NLTK, spaCy
Data Handling	Pandas
Visualization	Plotly
Media	pafy, youtube_dl
UI/UX	Custom CSS with animations
📦 Installation
1️⃣ Clone the repository
git clone https://github.com/yourusername/ResumeIQ.git
cd ResumeIQ

2️⃣ Create a virtual environment
python -m venv venv
source venv/bin/activate       # On macOS/Linux
venv\Scripts\activate          # On Windows

3️⃣ Install dependencies
pip install -r requirements.txt


Example dependencies:

streamlit
pandas
pyresparser
pdfminer.six
nltk
spacy
pymysql
plotly
pafy
youtube_dl
streamlit-tags
xlsxwriter

4️⃣ Setup database

Open MySQL and create the database:

CREATE DATABASE resumeiq;


Update database credentials in App.py:

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='your_password',
    database='resumeiq',
    port=3306
)


The app automatically creates required tables (user_data, admin_data, etc.) on first run.

▶️ Run the Application

Run Streamlit:

streamlit run App.py


Then open the local URL (usually http://localhost:8501
).

📊 Reports and Analytics

User Reports: Generated as Excel/CSV files after resume analysis

Admin Dashboard: Provides summarized analytics with visual charts

Data Export: All tables can be exported for HR or analysis use

📂 Project Structure
ResumeIQ/
│
├── App.py                   # Main Streamlit application
├── Courses.py               # Contains course recommendation data
├── Uploaded_Resumes/        # Stores uploaded resumes
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation

💡 Resume Scoring System

Each resume is scored out of 100 points based on the following criteria:

Section	Points
Objective	20
Declaration	20
Hobbies/Interests	20
Achievements	20
Projects	20
🧾 Example Output
User View

Upload a resume → Get field recommendation (e.g., Data Science)

See extracted skills and improvement suggestions

Download personalized Excel/CSV report

Watch YouTube learning videos

Admin View

Upload multiple resumes

Batch analyze and visualize data trends

Download complete datasets

🧰 Troubleshooting
Issue	Solution
nltk stopwords missing	Run import nltk; nltk.download('stopwords')
spacy model error	Run python -m spacy download en_core_web_sm
MySQL connection error	Check your credentials and ensure MySQL is running
Resume parsing failure	Ensure PDF text is selectable (not an image-based PDF)