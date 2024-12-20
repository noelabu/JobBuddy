import os
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from PyPDF2 import PdfReader
import docx

class ResumeAnalyzer:
    def __init__(self, api_key: str, resume_path:str):
        # Set the API key for OpenAI
        os.environ["OPENAI_API_KEY"] = api_key

        # Create a LangChain ChatOpenAI model
        self.llm = ChatOpenAI(
            model="gpt-4o-mini", 
            temperature=0.7,  # Slightly creative responses
            streaming=True
        )

        self.resume = resume_path

        self.system_prompt = SystemMessage(content="""You are an expert resume analyzer. Analyze the provided resume text and extract the following information:
            1. Contact Information (name, email, phone, LinkedIn)
            2. Professional Summary
            3. Skills (technical and soft skills)
            4. Work Experience (with duration and key achievements)
            5. Education
            6. Certifications
            7. Projects (if any)
            8. Areas of Expertise
            9. Career Highlights

            Also provide:
            1. Strengths of the resume
            2. Areas for improvement
            3. ATS compatibility score (0-100)
            4. Suggested improvements for ATS optimization

            Format the response as a JSON object. No json in the beginning.""")
    
    def _extract_text_from_pdf(self, file_path): 
        text = ""
        try:
            pdf_reader = PdfReader(file_path)
            for page in pdf_reader.pages:
                text += page.extract_text()
        except Exception as e:
            print(f"Error reading PDF: {e}")
        return text
    
    def _extract_text_from_docx(self, file_path):
        text = ""
        try:
            doc = docx.Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            print(f"Error reading DOCX: {e}")
        return text
    
    def _extract_text(self, file_name, file_path) -> str:
        if '.pdf' in file_name.name.lower():
            return self._extract_text_from_pdf(file_path)
        elif '.docx' in file_name.name.lower():
            return self._extract_text_from_docx(file_path)
        else:
            raise ValueError("Unsupported file format. Please provide PDF or DOCX file.")
    
    def analyze_resume(self, file_name, uploaded_file):
        resume_text = self._extract_text(file_name=file_name, file_path=uploaded_file)

        profile_messages = [
            self.system_prompt,
            HumanMessage(content=f"""
            Analyze the following professional profile and provide a summary:
            
            Profile Details:
            {resume_text}
            """)
        ]

        analysis_summary = self.llm.invoke(profile_messages)
        return analysis_summary.content


