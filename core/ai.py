import google.generativeai as genai
from datetime import date

genai.configure(api_key="AIzaSyANIfn9d0qroDzKMJXAUioA1dchI2ld5Jc")


def generate_ai_suggestions(tasks, user):
    model = genai.GenerativeModel('gemini-1.5-flash')
    today = date.today()

    try:
        profile = user.profile
        stage = profile.get_stage_display()
        program = profile.target_program if profile.target_program else "general competitive programs"
    except:
        stage = "Student"
        program = "competitive programs"

    task_details = ""
    for task in tasks:
        days_left = (task.due_date - today).days
        task_details += f"- {task.title} (Priority: {task.importance}, Due in {days_left} days)\n"

    prompt = f"""
    You are a high-tier Admissions & Career Consultant for a {stage} student.
    Target Program: {program}

    TASKS:
    {task_details if tasks else "No active tasks."}

    INSTRUCTIONS:
    1. Output EXACTLY 5 high-impact, hyper-specific suggestions.
    2. Focus on building a world-class profile for {program}.
    3. Be specific: Suggest actual organizations (e.g., FRC Robotics, USACO, DECA, IEEE) or specific technical projects.
    4. Mix 2 task-related tips with 3 "Profile Building" tips (competitions, internships, or high-level certifications).
    5. Each line must be under 15 words. No numbers, no bullets, no conversational filler.
    """

    try:
        response = model.generate_content(prompt)
        raw_lines = response.text.strip().split('\n')

        # Clean the lines from symbols and filter out short junk
        suggestions = []
        for line in raw_lines:
            clean = line.strip(" -*123456789.")
            if len(clean) > 8:
                suggestions.append(clean)

        while len(suggestions) < 5:
            suggestions.append(f"Research competitive summer programs for {program} specifically.")

        return suggestions[:5]
    except:
        return [
            "Prioritize your highest-impact assignments today.",
            f"Join a relevant competition team like FRC or DECA for {program}.",
            "Seek out a research assistant position in your target field.",
            "Complete a technical certification to boost your application resume.",
            "Maintain your GPA while building a unique project portfolio."
        ]