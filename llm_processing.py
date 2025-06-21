import database
import chroma_db
import os
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

def llm_response(query, user_id):
    docs = chroma_db.vector_db.similarity_search(
        query, 
        k=5,
        filter={"user_id": user_id}
    )
    context = "\n".join([doc.page_content for doc in docs])

    print(context)

    model = "mistral-large-latest"
    client = Mistral(api_key=MISTRAL_API_KEY)

    chat_response = client.chat.complete(
        model= model,
        messages = [
            {
                "role": "user",
                "content": f"Используй только этот контекст: {context}. Ответь на вопрос: {query}",
            },
        ]
    )

    return chat_response.choices[0].message.content