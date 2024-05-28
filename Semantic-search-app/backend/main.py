from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from weaviate import Client as WeaviateClient
from sentence_transformers import SentenceTransformer
import sys

app = FastAPI()
weaviate = WeaviateClient("http://weaviate:8080")
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter("%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

logger.info('API is starting up')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8030"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
def search(text_desc: str, video_desc: str, n_records: int, min_distance: float):
    print ("Text length: ", len(text_desc))
    print ("Video length: ", len(video_desc))
    print ("text_desc: ", text_desc)
    print ("video_desc: ", video_desc)

    if(len(text_desc) != 0 and len(video_desc) != 0):
        combined_text = f"In the video you can hear: {text_desc} In the video you can see: {video_desc}"
        vector = model.encode(combined_text)

        response = weaviate.query.get("Video_text_description", ["text", "starttime", "endtime", "metadata", "video_id"]) \
            .with_near_vector({"vector": vector, "distance":min_distance }) \
            .with_limit(n_records) \
            .with_additional(["distance"]) \
            .do()

        print(response)
        return response
    elif(len(text_desc) != 0):
        vector = model.encode(text_desc)
        response = weaviate.query.get("Video_text", ["text", "starttime", "endtime", "metadata", "video_id"]) \
            .with_near_vector({"vector": vector, "distance":min_distance }) \
            .with_limit(n_records) \
            .with_additional(["distance"]) \
            .do()
        
        print(response)
        return response
    else:
        vector = model.encode(video_desc)
        response = weaviate.query.get("Video_description", ["text", "starttime", "endtime", "metadata", "video_id"]) \
            .with_near_vector({"vector": vector, "distance":min_distance }) \
            .with_limit(n_records) \
            .with_additional(["distance"]) \
            .do()
        print(response)
        return response
        

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
