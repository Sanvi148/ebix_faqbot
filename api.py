from fastapi import FastAPI
from retrieval.retrieve import retrieve_chunks
from retrieval.qa_chain import generate_answer
from fastapi.middleware.cors import CORSMiddleware
from retrieval.cache import (
    get_cached_answer,
    store_answer
)
app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def home():
    return {"message": "Welcome to the FAQ Bot API. Use the / endpoint to get answers to your questions."}

@app.post("/chat")
def chat(data:dict):
    print("=" * 50)
    print("Request received")
    question=data["question"]
    print("Question:", question)
    cached_answer = get_cached_answer(question)
    print("Checking cache...")
    if cached_answer:

        print("CACHE HIT")

        return {
            "question": question,
            "answer": cached_answer,
            "context": "Retrieved from cache"
        }
    print("CACHE MISS")
    print("RETRIEVING CONTEXT")
    context = retrieve_chunks(question)
    print("Retreival complete")
    print("Context length:",len(context))
    print("Calling generate_answer()...")
    answer=generate_answer(question,context)
    print("Answer generated")
    print("Saving answer to cache...")
    store_answer(question, answer)
    print("Answer stored in cache")
    print("Answer generated successfully")
    print("=" * 50)
    return{
        "question": question,
        "answer": answer,
        "context": context,
    }