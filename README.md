# Agentic AI Rater

This project uses an AI agent to rate responses from a Google Form and generate cross-questions.

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare your CSV file

1.  Export your Google Form responses as a CSV file.
2.  Make sure the CSV file has the following columns:
    *   `You are tasked with identifying a suitable spe`
    *   `Share one creative idea you would implement`

### 3. Configure the Project

Open `config.py` and update the following variables:

*   `CSV_FILE_PATH`: The path to your input CSV file.
*   `OUTPUT_CSV_PATH`: The path where the results will be saved.
*   `GROQ_API_KEY`: Your Groq Cloud API key.
*   `MODEL_NAME`: The name of the Groq model you want to use (e.g., `llama3-8b-8192`).

### 4. Run the Script

```bash
python main.py
```

## How it Works

1.  The script reads all records from the specified CSV file.
2.  For each record, it extracts the answers from the two specified columns.
3.  It then uses a Groq model to rate each answer and generate a cross-question.
4.  The results are saved to the CSV file specified in `OUTPUT_CSV_PATH`.