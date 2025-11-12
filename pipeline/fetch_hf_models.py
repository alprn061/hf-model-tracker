import os
import requests
from dotenv import load_dotenv
from loguru import logger
from pipeline.normalize import normalize_model

# load .env file into memory
load_dotenv()

# define parameters
HF_TOKEN = os.getenv("HF_TOKEN")


def fetch_models(limit=5):
    """
    Get Hugging Face models
    """
    if not isinstance(limit, int) or limit < 1:
        limit = 5
    limit = min(limit, 50)
    API_URL =  f"https://huggingface.co/api/models?limit={limit}"
    headers = {}
    if HF_TOKEN:
        headers["Authorization"] = f"Bearer {HF_TOKEN}"

    try:
        resp = requests.get(API_URL, headers=headers, timeout=20)
        resp.raise_for_status()
        data =resp.json()
        logger.info(f"✅ Successfully fetched {len(data)} models from Hugging Face.")
        return data
    except requests.exceptions.Timeout:
        logger.error("⏱️ API request timed out.")
    except requests.exceptions.RequestException as e:
        logger.error(f"🌐 Network error: {e}")
    return []


# test
if __name__ == "__main__":
    from pipeline.normalize import normalize_model

    data = fetch_models(limit=3)
    if not data:
        print("No data fetched.")
    else:
        model = data[-1]
        model_row, tags, meta_row = normalize_model(model)

        print("\nMODEL_ROW:", model_row)
        print("\nTAGS:", tags[:5])
        print("\nMETA_ROW:", meta_row)