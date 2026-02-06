import os
from celery import Celery
import binascii
from .vision import extract_ingredients_from_image
from .matcher import get_matching_recipes

celery_app = Celery(
    "worker",
    broker=os.getenv("REDIS_URL", "redis://redis:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://redis:6379/0")
)

@celery_app.task(name="extract_ingredients_task")
def extract_ingredients_task(image_hex: str):
    # 1. Convert the hex string (from Redis) back into binary bytes
    image_bytes = binascii.unhexlify(image_hex)
    
    # 2. Call the Gemini Vision service
    ingredients = extract_ingredients_from_image(image_bytes)
    
    # 3. Return the real ingredients to be stored in the Redis backend
    return ingredients

@celery_app.task(name="match_recipes_task")
def match_recipes_task(ingredients):
    # Handle the case where the AI failed to find ingredients
    if not ingredients or "error" in ingredients:
        return {"error": "No ingredients found to match recipes."}
    
    # Run the Pinecone search
    recommendations = get_matching_recipes(ingredients)
    return {
        "ingredients": ingredients,
        "recommendations": recommendations
    }