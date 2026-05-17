from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestBody(BaseModel):
    regions: list[str]
    threshold_ms: int


# Robust path handling for Vercel
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "telemetry.json")

with open(DATA_FILE, "r") as f:
    telemetry = json.load(f)


def percentile_95(values):
    values = sorted(values)

    if not values:
        return 0

    index = int(0.95 * (len(values) - 1))
    return values[index]


@app.post("/")
def analyze(data: RequestBody):

    result = {}

    for region in data.regions:

        rows = [
            row for row in telemetry
            if row["region"] == region
        ]

        if not rows:
            continue

        latencies = [r["latency_ms"] for r in rows]
        uptimes = [r["uptime"] for r in rows]

        avg_latency = sum(latencies) / len(latencies)
        avg_uptime = sum(uptimes) / len(uptimes)

        p95_latency = percentile_95(latencies)

        breaches = sum(
            1 for x in latencies
            if x > data.threshold_ms
        )

        result[region] = {
            "avg_latency": round(avg_latency, 2),
            "p95_latency": round(p95_latency, 2),
            "avg_uptime": round(avg_uptime, 2),
            "breaches": breaches
        }

    return result