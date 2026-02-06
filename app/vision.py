from google import genai
from google.genai import types
import os
import json
from PIL import Image
import io

# 1. Initialize the new 2026 Client
# It automatically looks for 'GOOGLE_API_KEY' in your environment
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def extract_ingredients_from_image(image_bytes: bytes):
    try:
        # Convert bytes to a format the model understands
        image = Image.open(io.BytesIO(image_bytes))
        
        prompt = """
        Identify all food ingredients in this fridge/pantry photo. 
        Return ONLY a JSON list of strings.
        Example: ["milk", "eggs", "spinach"]
        """
        
        # 2. Call the Gemini 2.5 Flash model
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt, image]
        )
        
        # 3. Parse the result (2.5 models are much better at returning clean JSON)
        clean_json = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_json)

    except Exception as e:
        return {"error": f"Gemini 2.5 Extraction failed: {str(e)}"}