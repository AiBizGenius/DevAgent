import requests
import re
import json
from typing import Any, Dict
from pydantic import ValidationError
from models.groq_models import (
    InferenceRequest,
    InferenceResponse,
    CodeReviewRequest,
    CodeReviewFeedback,
    ChatCreateRequest,
    ChatCreateResponse
)

class GROQClient:
    def __init__(self, api_endpoint: str, api_key: str):
        self.api_endpoint = api_endpoint
        self.api_key = api_key

    def _post_chat_completion(self, model_id: str, messages: list[dict]) -> dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model_id,
            "messages": messages
        }
        response = requests.post(self.api_endpoint, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()

    def send_inference_request(self, model_id: str, input_data: Dict[str, Any]) -> InferenceResponse:
        try:
            json_response = self._post_chat_completion(model_id, input_data["messages"])
            return InferenceResponse.parse_obj(json_response)
        except ValidationError as e:
            print("Validation Error:", e)
            raise


    def send_code_review_request(self, model_id: str, code_review_request: CodeReviewRequest) -> CodeReviewFeedback:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a senior software engineer performing a code review. "
                    "Provide your response strictly in this JSON format:\n\n"
                    "{\n"
                    "  \"overall_quality\": \"string\",\n"
                    "  \"issues\": [ { \"description\": \"string\" } ],\n"
                    "  \"suggestions\": [ \"string\", ... ]\n"
                    "}\n\n"
                    "Be critical and cover bugs, design flaws, and bad practices."
                )
            },
            {
                "role": "user",
                "content": (
                    f"File Name: {code_review_request.file_name}\n\n"
                    f"Diff: {code_review_request.diff}\n\n"
                    f"Code:\n{code_review_request.file_content}"
                )
            }
        ]

        try:
            json_response = self._post_chat_completion(model_id, messages)
            content = json_response["choices"][0]["message"]["content"]
            print(content)

            # Attempt to parse valid JSON response directly
            try:
                parsed = json.loads(content)
                return CodeReviewFeedback(
                    overall_quality=parsed.get("overall_quality", "Unknown"),
                    issues=parsed.get("issues", []),
                    suggestions=parsed.get("suggestions", [])
                )
            except json.JSONDecodeError:
                print("⚠️ Model did not return valid JSON. Attempting fallback parsing...")

            # Fallback regex parsing
            overall_match = re.search(r"Overall Quality:\s*(.*)", content, re.IGNORECASE)
            overall_quality = overall_match.group(1).strip() if overall_match else "Unknown"

            issues = []
            issues_section = re.search(r"Issues:\s*((?:- .*\n?)*)", content, re.IGNORECASE)
            if issues_section:
                issue_lines = issues_section.group(1).strip().splitlines()
                issues = [{"description": line[2:].strip()} for line in issue_lines if line.startswith("- ")]

            suggestions = []
            suggestions_section = re.search(r"Suggestions:\s*((?:- .*\n?)*)", content, re.IGNORECASE)
            if suggestions_section:
                suggestion_lines = suggestions_section.group(1).strip().splitlines()
                suggestions = [line[2:].strip() for line in suggestion_lines if line.startswith("- ")]

            return CodeReviewFeedback(
                overall_quality=overall_quality,
                issues=issues,
                suggestions=suggestions
            )

        except ValidationError as e:
            print("❌ Validation Error:", e)
            raise
        except Exception as ex:
            print("❌ Unexpected Error:", ex)
            raise


    def send_chat_create_request(self, chat_create_request: ChatCreateRequest) -> ChatCreateResponse:
        messages = [
            {"role": "system", "content": chat_create_request.context},
            {"role": "user", "content": chat_create_request.user_message}
        ]
        try:
            json_response = self._post_chat_completion("llama3-8b-8192", messages)  # Replace with dynamic model if needed
            return ChatCreateResponse.parse_obj(json_response)
        except ValidationError as e:
            print("Validation Error:", e)
            raise
