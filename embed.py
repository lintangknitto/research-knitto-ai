from app.config.model_client import GENAI

text = "COMBED 30S"

result = GENAI.embed_content(model="models/text-embedding-004", content=text)

