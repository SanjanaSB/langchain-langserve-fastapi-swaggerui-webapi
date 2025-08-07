from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langserve import add_routes
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from langchain_community.llms import Ollama
from dotenv import load_dotenv

load_dotenv()

app=FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API Server"
)
# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


llm1=Ollama(model="qwen:7b")
prompt1=ChatPromptTemplate.from_template("Write me an essay about {topic} with 100 words")
llm2=Ollama(model="gemma3n")
prompt2=ChatPromptTemplate.from_template("Write me an poem about {topic} for a 5 years child with 100 words")
add_routes(
    app,
    prompt1|llm1,
    path="/essay"


)

add_routes(
    app,
    prompt2|llm2,
    path="/poem"


)

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__=="__main__":
    uvicorn.run(app,host="localhost",port=8001)
