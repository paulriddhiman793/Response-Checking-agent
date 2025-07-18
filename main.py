import csv
import groq
import re
from config import CSV_FILE_PATH, OUTPUT_CSV_PATH, GROQ_API_KEY, MODEL_NAME

def main():
    """
    Main function to read data from a CSV file, rate responses, and ask cross-questions.
    """
    # Configure the Groq client
    client = groq.Groq(api_key=GROQ_API_KEY)

    # Prepare to write to the output CSV file
    with open(OUTPUT_CSV_PATH, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["Name", "Answer 1", "Rating 1", "Cross-question 1", "Answer 2", "Rating 2", "Cross-question 2"])

        # Read the input CSV file
        with open(CSV_FILE_PATH, 'r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                name = row.get("Name")
                answer1 = row.get("You are tasked with identifying a suitable speaker for a guest lecture on a specific topic. Describe the approach you would take to carry out this responsibility. ")
                answer2 = row.get("Share one creative idea you would implement to increase event visibility and student engagement.")

                rating1, question1 = rate_and_question(client, answer1) if answer1 else ("N/A", "N/A")
                rating2, question2 = rate_and_question(client, answer2) if answer2 else ("N/A", "N/A")

                writer.writerow([name, answer1, rating1, question1, answer2, rating2, question2])

def rate_and_question(client, answer):
    """
    Uses the Groq model to rate an answer and generate a cross-question.
    """
    prompt = f"""
    Analyze the following answer and provide a rating and a cross-question.

    **Answer:**
    "{answer}"

    **Instructions:**
    1.  Rate the answer on a scale of 1 to 10. The rating should be a single number.
    2.  Provide a relevant and insightful cross-question based on the answer.

    **Output Format:**
    Rating: [Your rating]
    Cross-question: [Your question]
    """
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=MODEL_NAME,
        )
        response_text = chat_completion.choices[0].message.content.strip()
        
        # Use regex to find the rating and question
        rating_match = re.search(r"Rating:\s*(\d{1,2})", response_text)
        question_match = re.search(r"Cross-question:\s*(.*)", response_text, re.DOTALL)

        rating = rating_match.group(1) if rating_match else "N/A"
        question = question_match.group(1).strip() if question_match else "N/A"

        return rating, question
    except Exception as e:
        return f"Error: {e}", "Error processing the request."

if __name__ == "__main__":
    main()