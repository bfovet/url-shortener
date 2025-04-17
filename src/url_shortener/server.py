from fastapi import FastAPI
from pymongo import MongoClient


async def lifespan(app: FastAPI):
    app.mongodb_client = MongoClient(MONGO_CONNECTION_URI)
    app.database = app.mongodb_client[DB_NAME]
    print("Connected to the MongoDB database")
    yield
    app.mongodb_client.close()


app = FastAPI(lifespan=lifespan)


MONGO_CONNECTION_URI = "mongodb://127.0.0.1:27017"
DB_NAME = "url_shortener"


@app.get("/")
async def root():
    return {"message": "Welcome to my simple URL shortener"}
