import os
import httpx
from dotenv import load_dotenv

load_dotenv()

PRISM_HOST = os.getenv("PRISMTRACE_HOST")
PRISM_PROJECT_ID = os.getenv("PRISMTRACE_PROJECT_ID")
PRISM_API_KEY = os.getenv("PRISMTRACE_API_KEY")


def send_trace(symptom, response, pregnancy_week, latency_ms):

    url = f"{PRISM_HOST}/api/traces"

    headers = {
        "Content-Type": "application/json",
        "X-PRISMtrace-Key": PRISM_API_KEY
    }

    data = {
        "project_id": PRISM_PROJECT_ID,
        "model": "mothercare-ai",
        "input_messages": [
            {
                "role": "user",
                "content": symptom
            }
        ],
        "output_message": response,
        "latency_ms": latency_ms,
        "session_id": "mothercare-session",
        "agent_id": "mothercare-ai"
    }

    try:
        result = httpx.post(
            url,
            headers=headers,
            json=data,
            timeout=10
        )
        print("PRISM STATUS:", result.status_code)
        

        if result.status_code == 200:
            print("PRISM TRACE SENT SUCCESSFULLY")
        else:
            print("PRISM ERROR:", result.text)

        
    except Exception as e:
        print("PRISM ERROR:",e)

    