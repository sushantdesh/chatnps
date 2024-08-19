from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import chromadb

# Initialize ChromaDB client and create a collection
chroma_client = chromadb.PersistentClient(path="/gcs")

collection = chroma_client.get_or_create_collection(name="my_collection")

app = FastAPI()

# Define request models
class AddDataRequest(BaseModel):
    documents: list[str]
    ids: list[str]

class QueryRequest(BaseModel):
    query_texts: list[str]
    n_results: int

@app.post("/add_data")
async def add_data(request: AddDataRequest):
    try:
        collection.add(documents=request.documents, ids=request.ids)
        return {"status": "success", "message": "Data added successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/get_query")
async def get_query(request: QueryRequest):
    try:
        results = collection.query(query_texts=request.query_texts, n_results=request.n_results)
        return {"status": "success", "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# If running locally, you would use this:
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# For Docker, this is handled by the CMD in the Dockerfile
