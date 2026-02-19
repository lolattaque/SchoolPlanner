import os
import google.generativeai as genai
from datetime import date
from dotenv import load_dotenv

# Load the .env file from the root directory
load_dotenv()

# Fetch the key from the environment
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    print("Error: GEMINI_API_KEY not found in .env file.")


def generate_ai_suggestions(tasks, user):
    """
    Generates 5 hyper-specific academic and profile-building suggestions.
    """
    # Use the specific model string 'gemini-1.5-flash'
    model = genai.GenerativeModel('gemini-1.5-flash')
    today = date.today()

    try:
        profile = user.profile
        stage = profile.get_stage_display()
        # Uses the target_program field for hyper-specific tailoring
        program = profile.target_program if profile.target_program else "competitive programs"
    except:
        stage = "Student"
        program = "competitive programs"

    task_details = ""
    for task in tasks:
        days_left = (task.due_date - today).days
        task_details += f"- {task.title} (Priority: {task.importance}, Due in {days_left} days)\n"

    # Hyper-specific prompt focusing on competitive profile building like FRC/USACO
    prompt = f"""
    You are a high-tier Admissions Consultant for a {stage} student.
    Target Program/Goal: {program}

    CURRENT TASKS:
    {task_details if tasks else "No active school tasks."}

    INSTRUCTIONS:
    1. Output EXACTLY 5 lines of hyper-specific competitive advice.
    2. Suggest specific high-impact activities (e.g., FRC Robotics, USACO, DECA, Research Internships).
    3. Ensure suggestions are tailored to building a world-class application for {program}.
    4. No discovery projects. No conversational filler. No bullets or numbers.
    5. Max 15 words per line.
    """

    try:
        response = model.generate_content(prompt)
        raw_lines = response.text.strip().split('\n')

        suggestions = []
        for line in raw_lines:
            clean = line.strip(" -*0123456789.")
            if len(clean) > 8:
                suggestions.append(clean)

        while len(suggestions) < 5:
            suggestions.append(f"Seek specific mentorship or internships related to {program} immediately.")

        return suggestions[:5]

    except Exception as e:
        # Fallback to premade academic suggestions if API fails
        print(f"Gemini API Error: {e}")
        return [
            "Prioritize your high-importance tasks to protect your GPA.",
            f"Join a competition team like FRC or DECA to boost your {program} profile.",
            "Look for research opportunities or lab internships in your field.",
            "Start a technical side project that proves your skill in the field.",
            "Review long-term admission requirements for your target university programs."
        ]