import os
import google.generativeai as genai
import json
from config import Settings
from src.office_automation_api import OfficeAutomationAPI, save_plan_to_file

def main():
    settings = Settings()

    if not settings.api_key:
        print("Error: GEMINI_API_KEY is not set. Please set the environment variable or add it to a .env file.")
        return

    genai.configure(api_key=settings.api_key)

    model = genai.GenerativeModel(
        model_name=settings.model_name,
        generation_config=genai.types.GenerationConfig(
            temperature=settings.temperature,
            max_output_tokens=settings.max_tokens,
            response_mime_type="application/json"
        )
    )

    problem_description = """
    The AI agent needs to prepare a quarterly sales presentation.
    Task:
    1. Open 'Q4_Sales_Review.pptx'.
    2. Go to the third slide.
    3. Add a new bullet point under the existing 'Key Achievements' section: "Successfully onboarded 5 new enterprise clients."
    4. Find the slide titled 'Regional Performance' and ensure the title font size is 48pt. If not, update it.
    5. Save the updated presentation as 'Q4_Sales_Review_FINAL.pptx'.
    """

    prompt = f"""
    You are an AI assistant designed to help other AI agents programmatically interact with Microsoft Office files.
    Given a natural language task, generate a structured plan or pseudo-code using a hypothetical but robust 'office_automation_api'.
    The output should be a JSON object with a single top-level key 'plan', which contains a list of steps.
    Each step in the plan should be an object with an 'action' (e.g., 'open_presentation', 'add_bullet_point')
    and 'details' (e.g., 'file_path', 'slide_index', 'text', 'section_title', 'font_size').

    Task: {problem_description}

    Generate the plan for the given task.
    """

    print("Sending request to the Gemini model to generate an Office interaction plan...\n")
    try:
        response = model.generate_content(prompt)
        if response.text:
            plan_json = json.loads(response.text)
            print("--- Generated Office Interaction Plan (JSON) ---")
            print(json.dumps(plan_json, indent=2))
            print("\n--- End of Plan ---")
            save_plan_to_file(plan_json, 'generated_plan.json')
        else:
            print("No plan generated. The model response was empty.")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure your GEMINI_API_KEY is correctly set and network is available.")

if __name__ == "__main__":
    main()
