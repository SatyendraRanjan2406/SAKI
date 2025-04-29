import openai
from openai import OpenAI
from dotenv import load_dotenv
from SakiProject.settings import OPEN_AI_KEY
import json

# Use .env to store your API key or paste it directly into the code
load_dotenv()

prompt= """
    You are a professional recruiter building search criteria for sourcing talent across the web.
    
    You are given a user input that can be a text description, a list of skills, or a full job description.
    
    Your goal is to extract clear, structured search criteria based on the user input.
    
    Rules you must follow:
    
    Extract only the 2–5 most important criteria based on the user's input.
    
    If the user input is simple, use only 2–3 strong criteria (do not force 5).
    
    If the user input is complex, merge similar ideas logically using "and" or group related items into combined criteria (to fit inside 5 total).
    
    Criteria should be specific and actionable — focus on job title, skills, location, industry experience, years of experience, languages, or certifications.
    
    Prefer skills and industries first, then location, then experience, if you need to prioritize.
    
    Never create more than 5 criteria total.
    
    Always paraphrase the criteria in short, clear bullet points.
    
    Do not simply copy and paste the text — analyze and summarize into search-friendly points.
    Give output in form of pointed texts.
    
    You must return the response in the following JSON format:
    {
        "success": true,
        "message": [
            "First criteria (short and clear)",
            "Second criteria",
            "Third criteria",
            "Fourth criteria (optional if needed)",
            "Fifth criteria (optional if needed)"
        ]
    }
    
    Examples:
    
    User input:"Software engineer in SF who have 5+ years exp in Python, Django, worked in B2B SAAS"
    
    Output:
    {
        "success": true,
        "message": [
            "Currently or previously employed as a software engineer",
            "Located in San Francisco, CA",
            "At least 5 years of professional experience with Python and Django",
            "Professional experience in B2B SaaS industry"
        ]
    }
    
    User input:"Product manager with semiconductor industry experience, used analytical tools or data-driven decision making, located in Bay Area"
    
    Output:
    {
        "success": true,
        "message": [
            "Currently working as a product manager",
            "Professional experience in the semiconductor industry",
            "Demonstrated use of analytical tools or data-driven decision making",
            "Located in the Bay Area or San Francisco",
            "B2B SaaS experience"
        ]
    }
    """

client = openai.OpenAI(api_key=OPEN_AI_KEY)
def generate_search_criteria(query):
    try:
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": query}
        ]
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.2,
        )
        response = completion.choices[0].message.content
        
        # Try to parse the response as JSON
        try:
            response_data = json.loads(response)
            if isinstance(response_data, dict) and "message" in response_data:
                return response_data
            return {"success": False, "message": "Invalid response format"}
        except json.JSONDecodeError:
            return {"success": False, "message": "Failed to parse response as JSON"}
    except Exception as e:
        return {"success": False, "message": f"Error generating search criteria: {str(e)}"}