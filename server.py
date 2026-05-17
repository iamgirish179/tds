# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "fastapi",
#   "uvicorn",
# ]
# ///

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import csv

app = FastAPI()

# Enable CORS for all origins (GET requests from anywhere)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

CSV_FILE = "q-fastapi.csv"


def load_students():
    students = []

    with open(CSV_FILE, newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            students.append({
                "studentId": int(row["studentId"]),
                "class": row["class"]
            })

    return students


@app.get("/api")
async def get_students(class_: list[str] | None = Query(default=None, alias="class")):
    students = load_students()

    # Filter if class query params are provided
    if class_:
        students = [s for s in students if s["class"] in class_]

    return {"students": students}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)