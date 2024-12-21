# JobBuddy - AI-Powered Career Coach

JobBuddy is your **AI-powered personalized career coach** designed to empower job seekers and professionals alike. By leveraging intelligent agents, JobBuddy transforms your resume into actionable insights, helping you secure the best opportunities and achieve your career goals. Whether you're looking to optimize your resume, receive career advice, or practice for interviews, JobBuddy offers tailored solutions that match your professional needs.

## Features

### 1. **Resume Analyzer**
The Resume Analyzer agent parses and analyzes your resume to extract relevant skills, experiences, and qualifications. 

- **Resume Parsing:** Extracts structured data from your uploaded resume, such as skills, work experience, education, and achievements.
- **Skill Extraction:** Identifies key skills mentioned in your resume and suggests additional skills based on current job market trends.

### 2. **Job Recommender**
This agent matches your skills and preferences to job opportunities.

- **Job Matching:** Recommends job listings from various job portals that align with your skills, qualifications, and career goals.
- **Preference Filtering:** Customizes job recommendations based on your preferences, including location, industry, and job level.

### 3. **Mock Interview Guide**
Prepare for your interviews with the Mock Interview Guide.

- **Interview Questions Generator:** Generates a list of potential interview questions tailored to your skills and target job roles.
- **Role-Specific Scenarios:** Includes behavioral and technical questions relevant to the positions you're targeting.
- **Response Tips:** Provides tips and guidance on how to approach each question effectively.

### 4. **Career Coach**
Offers personalized career advice and recommendations to help you plan your professional growth.

- **Career Path Guidance:** Suggests potential career paths based on your skills and experiences.
- **Goal Setting:** Helps you set achievable short-term and long-term career goals.
- **Action Plan:** Recommends actionable steps to progress in your chosen career path.

### 5. **Upskilling Recommender**
Identifies skill gaps and provides resources to help bridge them.

- **Skill Gap Analysis:** Compares your skills to the requirements of your desired roles and identifies areas for improvement.
- **Learning Recommendations:** Provides links to online courses, certifications, and workshops to enhance your skills.


## Key Features

- **Resume Parsing:** Effortlessly extract structured data from resumes and identify key skills.
- **Job Matching:** Receive job recommendations that are tailored to your profile and preferences.
- **Mock Interview Preparation:** Practice with customized interview questions and role-specific scenarios.
- **Career Guidance:** Get personalized advice on career paths, goals, and strategies for success.
- **Upskilling Recommendations:** Discover the best resources to improve your skills and stay competitive.


## How to Use JobBuddy

1. **Enter Your OpenAI API Key**  
   To use the platform, input your OpenAI API Key in the sidebar.

2. **Upload Your Resume**  
   Upload your resume to get started. JobBuddy will analyze your resume and provide tailored insights.

3. **Explore Career Tools**  
   Choose from a variety of tools available:
   - **Resume Analyzer:** Review your resume’s skills and experiences.
   - **Job Recommender:** Get job suggestions based on your profile.
   - **Mock Interview Guide:** Practice answering personalized interview questions.
   - **Career Coach:** Get expert advice and actionable career development steps.
   - **Upskilling Recommender:** Identify skill gaps and learn how to fill them with curated resources.

## Technologies Used

- **Streamlit**: For building the web app interface.
- **Langchain**: To interact with OpenAI models and generate insights.
- **OpenAI GPT Models**: For career advice, resume analysis, and job matching.
- **Python**: The core programming language for backend logic.

## Getting Started

To run the JobBuddy locally, clone this repository and install the necessary dependencies:

```bash
git clone https://github.com/noelabu/JobBuddy.git
cd JobBuddy
pip install -r requirements.txt
```

### API Key Configuration
To use the OpenAI API, you'll need an API key. Sign up at [OpenAI](https://openai.com) and create an API key. Store your key in an environment variable named `OPENAI_API_KEY`.

```bash
export OPENAI_API_KEY='your-api-key'
```

### Running the Streamlit App
After setting up the API key, you can run the Streamlit app to interact with the tools.

```bash
streamlit run app.py
```

Open your browser and go to `http://localhost:8501` to access the application. You can also access the application [here](https://noelabu-jobbuddy.streamlit.app/).

## Contributing

We welcome contributions to enhance JobBuddy! If you’d like to improve the platform, please fork the repository and create a pull request.