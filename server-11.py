# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "fastapi",
#   "uvicorn",
#   "transformers",
#   "torch",
# ]
# ///

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from transformers import pipeline

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load HuggingFace sentiment model
classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

class SentimentRequest(BaseModel):
    sentences: list[str]


def convert_label(label: str) -> str:
    """
    Convert model labels to required labels
    """
    if label == "POSITIVE":
        return "happy"

    if label == "NEGATIVE":
        return "sad"

    return "neutral"


@app.post("/sentiment")
async def sentiment(req: SentimentRequest):

    predictions = classifier(req.sentences)

    results = []

    for sentence, pred in zip(req.sentences, predictions):

        sentiment = convert_label(pred["label"])

        # Optional confidence threshold
        if pred["score"] < 0.60:
            sentiment = "neutral"

        results.append({
            "sentence": sentence,
            "sentiment": sentiment
        })

    return {"results": results}


@app.get("/")
async def root():
    return {"message": "Sentiment API running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)