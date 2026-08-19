import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# CRITICAL FOR GITHUB ACTIONS:
# Remove runner-injected GCP variables forcing OAuth2
os.environ.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
os.environ.pop("CLOUDSDK_AUTH_CREDENTIALS_INLINE_JSON", None)

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash-lite"
)

def ask_gemini(prompt):
    response = model.generate_content(
        prompt
    )
    return response.text