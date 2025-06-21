from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

model_name = "ai-forever/sbert_large_nlu_ru"
model_kwargs = {'device': 'cuda'}
encode_kwargs = {'normalize_embeddings': True}

embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

vector_db = Chroma(
    collection_name="user_notes",
    embedding_function=embeddings,
    persist_directory="db/chroma"
)

def save_vectorized_note(user_id: int, content: str): # Returns chuck ids
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(content)
    metadatas = [{"user_id": user_id} for _ in chunks]

    chunk_ids = vector_db.add_texts(
    texts=chunks,
    metadatas=metadatas,
    return_ids=True
    )

    return chunk_ids
