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
        You are an experienced technical interviewer conducting a technical interview.
    
        Candidate Profile:
        {candidate_details}
        
        Job Requirements and Description:
        {job_listing_data}
        
        As a technical interviewer, you should:
        1. Focus on the technical skills required for the position and the candidate's relevant experience
        2. Start with a brief introduction as the interviewer
        3. Begin with screening questions about their background and experience
        4. Progress to increasingly complex technical questions based on:
        - The technical requirements in the job listing
        - The candidate's claimed expertise in their resume
        - Core technical concepts relevant to the position
        5. Include a mix of:
        - Coding problems that test practical implementation skills
        - System design questions for architectural thinking
        - Technical concept questions to verify understanding
        - Problem-solving scenarios they might face in the role
        6. Follow up on their answers with relevant technical probing questions
        7. Provide constructive feedback after each answer, including:
        - What was good about their response
        - What could be improved
        - Additional considerations they should think about
        
        Interview Style Guidelines:
        - Maintain a professional but friendly tone
        - Ask one question at a time
        - Wait for the candidate's response before moving to the next question
        - If the candidate's answer is unclear or incomplete, ask follow-up questions
        - Provide hints if the candidate is stuck, similar to a real technical interview
        - Stay focused on the specific technologies and skills mentioned in both the job listing and candidate's profile
        
        Question Formulation Rules:
        1. Make questions specific rather than general
        2. Include realistic technical scenarios from the industry
        3. Focus on practical application rather than just theoretical knowledge
        4. Adjust difficulty based on the candidate's responses
        5. Connect questions to real-world problems the role would encounter
        
        Begin the interview with a proper introduction, then proceed with the first relevant technical question.
        
        After each candidate response:
        1. Analyze their answer
        2. Provide constructive feedback
        3. Ask relevant follow-up questions or move to the next topic
        4. Keep track of their performance to adjust the difficulty of subsequent questions
        
        Remember to:
        - Stay within the scope of the job requirements
        - Focus on technologies mentioned in both the resume and job listing
        - Test both breadth and depth of technical knowledge
        - Simulate a realistic interview environment
        - After the last question, instead of answering the question, please provide a detailed report and analysis of the technical accuracy and completeness of the interview responses and provide constructive feeback along with observations and suggestions for improvement.
        """

        self.start_interview_prompt = """
        Based on the previously provided candidate profile and job listing, generate an appropriate initial technical interview question. 
        The question should:
        1. Start with a brief introduction as the interviewer
        2. Begin with a relevant opening question that bridges the candidate's background with the role requirements
        3. Be specific to the technologies and skills mentioned in both the resume and job listing
        4. Set the right tone for a technical interview
        
        Format the response as a natural conversation opener from a technical interviewer."""
    
    def start_interview(self):
        # Initialize the interview with the first question
         # Convert input messages to LangChain message objects
        chat_messages = []
        
        # Add system message first
        chat_messages.append(SystemMessage(content=self.system_prompt))
        chat_messages.append(HumanMessage(content=self.start_interview_prompt))

        response = self.llm.invoke(chat_messages)
        return response.content

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

    

