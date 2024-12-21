import streamlit as st
from streamlit_option_menu import option_menu
from io import BytesIO
import json

from utils.mock_interview import MockInterview
from utils.job_post_summarizer import JobScraper
from utils.career_coach import CareerBoost
from utils.resume_analyzer import ResumeAnalyzer
from decouple import config

# Setting up the page configuration
st.set_page_config(page_title="Noela's JobBuddy", page_icon="💼", layout="wide")

# Sidebar input for API Key and resume upload
api_key_input = st.sidebar.text_input("Enter your OpenAI API Key:", type="password")
uploaded_file = st.sidebar.file_uploader("Upload your Resume:")

# Check if the input is the special keyword to load the API key from the environment
if api_key_input == config("USERNAME_SECRET"):
    api_key = config("OPENAI_API_KEY")  # Retrieve the API key from the environment variable
    if api_key is None:
        st.warning("API key is not set in the environment. Please set it and try again.")
else:
    api_key = api_key_input

# Sidebar navigation
with st.sidebar:
    page = option_menu(
        "JobBuddy",
        ["Home", "About Me", "Talk to a Career Coach", "Career Growth Recommendation", "Interview Questions", "Mock Interview"],
        icons=['house', 'person-circle', 'chat', 'briefcase', 'paperclip', 'mic'],
        menu_icon="list",
        default_index=0,
    )

# Function to initialize the ResumeAnalyzer and return the resume details
@st.cache_data
def analyze_resume(api_key, uploaded_file):
    uploaded_file_bytes = BytesIO(uploaded_file.read())
    resume_analyzer = ResumeAnalyzer(api_key=api_key, resume_path=uploaded_file)
    resume_details = resume_analyzer.analyze_resume(file_name=uploaded_file, uploaded_file=uploaded_file_bytes)
    return resume_details

# Function to initialize the CareerBoost instance
@st.cache_resource
def initialize_career_coach(api_key, resume_details):
    return CareerBoost(api_key=api_key, candidate_profile=resume_details)

# Check if uploaded file are available
if not api_key:
    st.warning("Please enter your OpenAI API Key in the sidebar to use the application.")
elif not uploaded_file:
    st.warning("Please upload your resume in the sidebar to use the application.")
elif uploaded_file:
    # Initialize resume details and career coach (this will only run once per session)
    resume_details = analyze_resume(api_key, uploaded_file)
    career_coach = initialize_career_coach(api_key, resume_details)

    # Home page content
    if page == "Home":
        st.title("JobBuddy")
        st.write("""
        JobBuddy is your AI-powered personalized career coach. Designed to empower job seekers and professionals, the platform provides tailored insights into job opportunities, career growth, and skill development. 
        With its intelligent agents, JobBuddy transforms your resume into actionable insights to help you secure the best opportunities and achieve your career goals.
        """)

        # Detailed feature explanation
        st.markdown("### 1. Resume Analyzer")
        st.write("**Purpose:** The Resume Analyzer agent parses and analyzes the user's resume to extract relevant skills, experiences, and qualifications.")
        st.write("""
        - **Resume Parsing:** Extracts structured data from the uploaded resume, such as skills, work experience, education, and achievements.
        - **Skill Extraction:** Identifies key skills mentioned in the resume and suggests additional skills based on the job market trends.
        """)

        st.markdown("### 2. Job Recommender")
        st.write("**Purpose:** This agent matches the user's skills and preferences to job opportunities.")
        st.write("""
        - **Job Matching:** Recommends job listings from various job portals that align with the user's skills, qualifications, and career goals.
        - **Preference Filtering:** Customizes job recommendations based on user preferences, such as location, industry, and job level.
        """)

        st.markdown("### 3. Mock Interview Guide")
        st.write("**Purpose:** Prepares users for interviews by generating targeted questions based on their resume and job listings.")
        st.write("""
        - **Interview Questions Generator:** Creates a list of potential interview questions tailored to the user's skills and target job roles.
        - **Role-Specific Scenarios:** Includes behavioral and technical questions relevant to the desired positions.
        - **Response Tips:** Provides tips and guidance on how to approach each question effectively.
        """)

        st.markdown("### 4. Career Coach")
        st.write("**Purpose:** Offers career advice and personalized recommendations to help users plan their professional growth.")
        st.write("""
        - **Career Path Guidance:** Suggests potential career paths based on the user's skills and experiences.
        - **Goal Setting:** Helps users set achievable short-term and long-term career goals.
        - **Action Plan:** Recommends actionable steps to progress in the chosen career path.
        """)

        st.markdown("### 5. Upskilling Recommender")
        st.write("**Purpose:** Identifies skill gaps and suggests resources to bridge them.")
        st.write("""
        - **Skill Gap Analysis:** Compares the user's skills to the requirements of their desired roles and identifies areas for improvement.
        - **Learning Recommendations:** Provides links to online courses, certifications, and workshops to enhance skills.
        """)

        st.subheader("Key Features")
        st.write("""
        - **Resume Parsing:** Effortlessly extract structured data from resumes and identify key skills.
        - **Job Matching:** Get job recommendations tailored to your profile and preferences.
        - **Mock Interview Preparation:** Practice with customized interview questions and role-specific scenarios.
        - **Career Guidance:** Receive personalized advice on career paths, goals, and strategies for success.
        - **Upskilling Recommendations:** Find the best resources to improve your skills and stay competitive.
        """)

    elif page == "About Me":
        st.header("About Me")
        st.markdown("""
        Hi! I'm Noela Jean Bunag, a Python Developer and AI Enthusiast. I'm passionate about creating accessible AI solutions and exploring the possibilities of Natural Language Processing.
        
        Connect with me on [LinkedIn](https://www.linkedin.com/in/noela-bunag/) to discuss AI, Python development, or potential collaborations.
        
        Check out my portfolio at [noelabu.github.io](https://noelabu.github.io/) to see more of my projects and work.
        """)

    elif page == "Talk to a Career Coach":
        # Initialize chat history if not present
        if "messages" not in st.session_state:
            st.session_state.messages = []

            # Extract user's name from resume details (ensure it's available)
            resume_details =  json.loads(resume_details)
            user_name = resume_details.get("Contact Information", {}).get('Name', 'there')   # Default to "there" if no name found

            # Define multiple initial personalized messages for Career Coach
            initial_messages = [
                f"Hello {user_name}! I'm your Career Coach. I'm here to help you plan your professional journey and set meaningful career goals. How would you like to shape your future?",
                f"Hi {user_name}! I'm your Career Coach. Let's work together to unlock your full potential and guide you towards your ideal career path. What do you want to focus on today?",
                f"Hey {user_name}! It's great to meet you. I'm here to assist you with career advice, growth strategies, and goal setting. What part of your professional development would you like to explore today?",
                f"Welcome {user_name}! As your Career Coach, my goal is to help you navigate your career path and set impactful goals. How can I support your growth today?",
                f"Hello {user_name}! I'm excited to be your Career Coach. Whether it's skill development, career planning, or goal setting, I can help you chart a path to success. What's on your mind?"
            ]

            # Pick a random initial message
            import random
            initial_message = random.choice(initial_messages)

            st.session_state.messages.append({"role": "assistant", "content": initial_message})


        # Display previous chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Accept user input for chat with the career coach
        if prompt := st.chat_input("Talk to your career coach!"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

            # Display assistant's response
            with st.chat_message("assistant"):
                response = st.write_stream(career_coach.career_coach_chat(st.session_state.messages))


            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    elif page == "Career Growth Recommendation":
        #career_recommend =  career_coach.generate_career_recommendation()
        st.write_stream(career_coach.generate_career_recommendation())
    
    elif page == "Interview Questions":
        st.header("Interview Questions Guide")
        job_list_url = st.text_input("Enter the url of the job_listing:")
        if st.button("Generate"):
            job_scraper=JobScraper(api_key=api_key)
            job_post_data = job_scraper.parse_job_listing(job_list_url=job_list_url)
            mock_int = MockInterview(api_key=api_key, candidate_details=resume_details, job_listing_data=job_post_data)
            st.write_stream(mock_int.generate_interview_questions())

    elif page == "Mock Interview":
        st.header("Mock Interview")
        st.write('To start, please enter the job listing URL to begin the interview.')

        # Check if job listing data is already stored in session state
        if "job_post_data" not in st.session_state:
            job_list_url = st.text_input("Enter the URL of the job listing:")
            
            if st.button("Start the mock interview"):
                # If the button is pressed and job listing is not yet parsed
                if job_list_url:
                    # Parse job listing and store it in session state
                    job_scraper = JobScraper(api_key=api_key)
                    job_post_data = job_scraper.parse_job_listing(job_list_url=job_list_url)
                    st.session_state.job_post_data = job_post_data
                else:
                    st.warning("Please enter a valid job listing URL.")
        else:
            # If job data is already present, don't parse again
            job_post_data = st.session_state.job_post_data

        if "job_post_data" in st.session_state:
            # Now, initiate the mock interview with the parsed job data and resume details
            mock_int = MockInterview(api_key=api_key, candidate_details=resume_details, job_listing_data=job_post_data)

            # Initialize chat history if not present
            if "interview" not in st.session_state:
                st.session_state.interview = []

                response = mock_int.start_interview()
                st.session_state.interview.append({"role": "assistant", "content": response})

            # Display previous chat messages
            for message in st.session_state.interview:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # Accept user input for chat in the mock interview
            if prompt := st.chat_input("Enter your answer:"):
                # Add user message to chat history
                st.session_state.interview.append({"role": "user", "content": prompt})

                # Display user message in chat message container
                with st.chat_message("user"):
                    st.markdown(prompt)

                # Display assistant's response
                with st.chat_message("assistant"):
                    response = st.write_stream(mock_int.mock_interview_chat(st.session_state.interview))

                # Add assistant response to chat history
                st.session_state.interview.append({"role": "assistant", "content": response})
