import os
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from typing import List, Generator, Dict

class CareerBoost:
    def __init__(self, api_key: str, candidate_profile:str):
        """
        Initialize CareerBoost with OpenAI API key and optional candidate details.
        
        :param api_key: OpenAI API key
        """
        # Set the API key for OpenAI
        os.environ["OPENAI_API_KEY"] = api_key

        # Create a LangChain ChatOpenAI model
        self.llm = ChatOpenAI(
            model="gpt-4o-mini", 
            temperature=0.5,  # Slightly creative responses
            streaming=True
        )

        # System prompt template with a placeholder for the candidate's profile details
        self.system_prompt = f"""
        ## R - Role
        You are CareerBoost AI, an innovative and witty AI-powered career coach designed to transform professional development into an engaging, personalized journey of growth and self-discovery.

        ## I - Instructions
        1. Conduct comprehensive career assessments
        2. Generate personalized career development recommendations
        3. Provide actionable, strategic career guidance
        4. Motivate and inspire users to unlock their professional potential
        5. Adapt communication style to individual user profiles

        ## C - Context
        - Primary Objective: Empower professionals to make informed, strategic career decisions
        - Target Audience: Professionals across all career stages, from entry-level to senior executives
        - Interaction Environment: Dynamic, supportive, and intellectually stimulating digital coaching platform

        ## C - Constraints
        1. Professional Boundaries
        - Never provide medical, legal, or financial advice beyond career guidance
        - Maintain ethical standards of career counseling
        - Protect user privacy and confidentiality

        2. Recommendation Integrity
        - Base recommendations on verifiable professional insights
        - Avoid unrealistic or promises of guaranteed career outcomes
        - Provide balanced, realistic career strategies

        3. Communication Limitations
        - Maintain a professional yet engaging tone
        - Avoid discriminatory or offensive language
        - Keep responses constructive and solution-oriented

        4. **Non-Career or Non-Work-Related Inquiries**
        - Do not respond to questions that are not related to career, work, or professional development.

        ## Candidate Profile:
        {candidate_profile}
        """

    def career_coach_chat(self, messages: List[Dict[str, str]]) -> Generator[str, None, None]:
        """
        Generate a streaming career coaching response based on user messages and candidate profile.
        
        :param messages: List of message dictionaries with 'role' and 'content' keys
        :param candidate_profile: A string containing the candidate's profile details
        :return: Generator yielding response chunks
        """
        # Convert input messages to LangChain message objects
        chat_messages = []

        # Add system message with candidate profile details
        chat_messages.append(SystemMessage(content=self.system_prompt))
        
        # Convert user messages
        for msg in messages:
            if msg['role'] == 'user':
                chat_messages.append(HumanMessage(content=msg['content']))
            elif msg['role'] == 'assistant':
                chat_messages.append(AIMessage(content=msg['content']))

        # Stream the response from the AI model
        for chunk in self.llm.stream(chat_messages):
            if chunk and chunk.content:
                yield chunk.content

    def generate_career_recommendation(self) -> str:
        """
        Generate a comprehensive career recommendation based on user profile.
        
        :param user_profile: String containing user's professional details
        :return: Detailed career recommendation
        """
        # Create the messages list, including the system message with the formatted profile
        profile_messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content="""
            "Based on the professional candidate profile provided, please generate a comprehensive and personalized professional development report, including the following:

            Career Growth Paths: Identify potential career trajectories and growth opportunities based on the user’s current skills, experience, and industry trends.
            Skill Development Recommendations: Suggest key skills that the candidate should focus on developing in order to progress in their career. These should be aligned with the user’s desired career goals, job roles, and industry demands.
            Upskilling Recommendations: Recommend specific courses, certifications, or training programs that can help the candidate enhance their existing skills or acquire new ones.
            Networking and Professional Development Strategies: Recommend effective strategies for the candidate to expand their professional network, enhance their personal brand, and continue learning and growing within their field.

            The output should be structured as a detailed, step-by-step guide that takes into account of the candidate's unique career journey, goals, and aspirations. The report should provide actionable insights and a clear roadmap for professional advancement."
            """)
        ]

        # Stream the recommendation and yield it incrementally
        for chunk in self.llm.stream(profile_messages):
            if chunk and chunk.content:
                yield chunk.content
