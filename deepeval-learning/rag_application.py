import os
from dotenv import load_dotenv
from google import genai
from knowledge_base import retrieve_documents

load_dotenv()

client = genai.Client(
    api_key=os.environ["GOOGLE_API_KEY"]
)

MODEL = "gemini-3.5-flash-lite"

def ask_hr_bot(question):
    documents = retrieve_documents(question)
    context = "\n".join(documents)

    prompt = f"""
    You are an HR policy assistant.

    Answer using only the provided context.
    If the answer is unavailable, say:
    "I don't have that information."

    Context:
    {context}

    Question: 
    {question}
    """

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text or "", documents