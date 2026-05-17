from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import numpy as np

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Load telemetry data once
with open("telemetry.json", "r") as f:
    telemetry = json.load(f)


class RequestBody(BaseModel):
    regions: list[str]
    threshold_ms: int


@app.post("/")
def analyze(data: RequestBody):

    result = {}

    for region in data.regions:

        region_rows = [
            row for row in telemetry
            if row["region"] == region
        ]

        if not region_rows:
            continue

        latencies = [r["latency_ms"] for r in region_rows]
        uptimes = [r["uptime"] for r in region_rows]

        avg_latency = sum(latencies) / len(latencies)

        p95_latency = float(np.percentile(latencies, 95))

        avg_uptime = sum(uptimes) / len(uptimes)

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