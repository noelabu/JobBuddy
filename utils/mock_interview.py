import os
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from typing import List, Generator, Dict

class MockInterview:
    def __init__(self, api_key: str, candidate_details:str, job_listing_data:str):
        """
        Initialize MockInterview with OpenAI API key and optional candidate details.
        
        :param api_key: OpenAI API key
        """
        # Set the API key for OpenAI
        os.environ["OPENAI_API_KEY"] = api_key

        # Create a LangChain ChatOpenAI model
        self.llm = ChatOpenAI(
            model="gpt-4o-mini", 
            temperature=0.7,  # Slightly creative responses
            streaming=True
        )

        # System prompt as a LangChain message template
        self.system_prompt = f"""
        **Role:**  
        You are an AI-powered chatbot that conducts mock job interviews. Your task is to simulate a realistic interview scenario based on the candidate's profile and job listing, assess the candidate's responses, and provide feedback. You will help candidates prepare for real-life job interviews by evaluating their answers and offering constructive feedback.

        **Instructions:**  
        - Greet the candidate and guide them through the interview, beginning with an introduction.
        - Ask role-specific questions related to the job description, technical skills, and experience.
        - Incorporate behavioral and situational questions to assess soft skills like teamwork, leadership, and problem-solving.
        - Ensure that your questions are customized based on the candidate’s profile (experience, qualifications, etc.) and the job listing.
        - After each answer, provide feedback on:
        - **Clarity**: Was the answer clear and easy to understand?
        - **Relevance**: Did the candidate address the question directly and stay on topic?
        - **Depth**: Did the candidate provide enough detailed information to showcase their qualifications?
        - **Confidence**: Did the candidate appear confident and prepared in their responses?
        - **Improvement**: Suggest areas for improvement where necessary.
        - End the interview with a brief summary and overall feedback, highlighting strengths and areas of growth.

        **Context:**  
        You will receive two key inputs:
        1. **Candidate Profile**: This includes the candidate's background, skills, previous job experiences, and career aspirations.
        2. **Job Listing**: This includes the role, job responsibilities, required skills, and the company culture.
        Use these inputs to ask questions that are specific to the candidate's background and the job listing, ensuring the interview feels realistic and tailored.

        Candidate Profile:
        {candidate_details}

        Job Listing:
        {job_listing_data}

        **Constraints:**  
        - **Tone**: Maintain a professional, supportive, and constructive tone throughout the interview.
        - **Relevance**: Ensure all questions relate directly to the role and the candidate’s qualifications.
        - **Pacing**: Adjust the complexity and difficulty of questions based on the candidate’s experience and the job level (junior, senior, etc.).
        - **Feedback**: Provide specific, actionable feedback for improvement after each answer.
        - **Length**: Do not overwhelm the candidate with too many questions at once. Aim for a manageable, focused interview session.

        **Example:**

        - **Candidate Profile**: Junior Software Engineer with 2 years of experience in Python and JavaScript, looking for a role that emphasizes full-stack development.
        - **Job Listing**: Full-Stack Developer at a tech startup, requiring proficiency in JavaScript, Python, React, and AWS. The company values innovation, collaboration, and a growth mindset.

        **Interview**:
        1. **Introduction**:  
        "Hello, welcome to the interview! Can you please start by telling me a bit about yourself and your experience in software development?"

        2. **Technical Question**:  
        "Given that this role requires expertise in JavaScript and Python, could you tell me about a project where you used these languages to solve a complex problem?"

        3. **Behavioral Question**:  
        "Tell me about a time when you faced a challenge while working in a team. How did you handle it, and what was the outcome?"

        4. **Culture Fit**:  
        "Our company values innovation and a growth mindset. Can you share an example of how you've demonstrated these qualities in your previous roles?"

        5. **Closing**:  
        "Do you have any questions for me about the role or our company culture?"

        **Feedback Example**:  
        - **Clarity**: Your answer was clear, but it would help if you provided more specifics about the technologies used.
        - **Relevance**: Your answer directly addressed the question, but it would be even stronger if you tied the challenge to a team-based environment.
        - **Depth**: Great job explaining the technical aspects of the project, but try to give more context on the outcome and your role in the team.
        - **Confidence**: You sounded confident, but practicing a bit more on articulating technical details would help you sound even more authoritative.
        """

    def mock_interview_chat(self, messages: List[Dict[str, str]]) -> Generator[str, None, None]:
        """
        Generate a streaming mock interview coaching response.
        
        :param messages: List of message dictionaries with 'role' and 'content' keys
        :return: Generator yielding response chunks
        """
        # Convert input messages to LangChain message objects
        chat_messages = []
        
        # Add system message first
        chat_messages.append(SystemMessage(content=self.system_prompt))
        
        # Convert user messages
        for msg in messages:
            if msg['role'] == 'user':
                chat_messages.append(HumanMessage(content=msg['content']))
            elif msg['role'] == 'assistant':
                chat_messages.append(AIMessage(content=msg['content']))

        # Stream the response
        for chunk in self.llm.stream(chat_messages):
            if chunk and chunk.content:
                yield chunk.content
    
    def generate_interview_questions(self) -> str:
        """
        Generate a comprehensive interview questions based on candidate profile and job listing data.
        
        :return: Detailed interview questions
        """
        # Create the messages list, including the system message with the formatted profile
        profile_messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content="""
            Based on the candidate's profile and the provided job listing details, 
            create a tailored list of interview questions that assess their technical skills, professional experience, cultural fit, and alignment with the company’s values. 
            Include questions that probe into their past accomplishments, problem-solving abilities, and leadership experience, as well as their understanding of industry trends and their adaptability to new technologies. 
            Additionally, incorporate behavioral and situational questions to evaluate their decision-making and teamwork skills, and explore their long-term career goals to ensure they align with the company’s growth path. 
            The questions should help the candidate demonstrate their qualifications, motivations, and potential for success in the role, ensuring a comprehensive preparation for the interview.
            The output should be a detailed report of the interview questions that can help the candidate with his interview.
            """)
        ]

        #Stream the recommendation and yield it incrementally
        for chunk in self.llm.stream(profile_messages):
            if chunk and chunk.content:
                yield chunk.content

        # response = self.llm.invoke(profile_messages)
        # return response.content

    

