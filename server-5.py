from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from google import genai
from google.genai import types

import os
import sys
import traceback
from io import StringIO

# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI()

# -----------------------------
# Enable CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Request / Response Models
# -----------------------------
class CodeRequest(BaseModel):
    code: str


class CodeResponse(BaseModel):
    error: List[int]
    result: str


class ErrorAnalysis(BaseModel):
    error_lines: List[int]


# -----------------------------
# Tool Function
# -----------------------------
def execute_python_code(code: str) -> dict:
    """
    Execute Python code and return exact output.
    """

    old_stdout = sys.stdout
    old_stderr = sys.stderr

    sys.stdout = StringIO()
    sys.stderr = StringIO()

    try:
        # Execute code
        exec(code)

        output = sys.stdout.getvalue()

        return {
            "success": True,
            "output": output
        }

    except Exception:
        # Exact traceback
        output = traceback.format_exc()

        return {
            "success": False,
            "output": output
        }

    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr


# -----------------------------
# AI Error Analysis
# -----------------------------
import re

def analyze_error_with_ai(code: str, traceback_text: str):

    matches = re.findall(
        r'File "<string>", line (\d+)',
        traceback_text
    )

    if not matches:
        return []

    # Actual error line is usually the last user-code frame
    return [int(matches[-1])]


# -----------------------------
# API Endpoint
# -----------------------------
@app.post("/code-interpreter", response_model=CodeResponse)
def code_interpreter(request: CodeRequest):

    execution_result = execute_python_code(request.code)

    # Success case
    if execution_result["success"]:
        return CodeResponse(
            error=[],
            result=execution_result["output"]
        )

    # Error case -> invoke AI
    error_lines = analyze_error_with_ai(
        request.code,
        execution_result["output"]
    )

    return CodeResponse(
        error=error_lines,
        result=execution_result["output"]
    )


# -----------------------------
# Run Server
# -----------------------------
# Run with:
# uvicorn main:app --reload
#
# Then expose using ngrok:
# ngrok http 8000
#
# Endpoint:
# https://YOUR_NGROK_URL/code-interpreter