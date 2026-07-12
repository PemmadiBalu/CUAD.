
from groq import Groq
from flask import current_app


class LLMProcessor:

    def __init__(self):
        self.client = None

    def _get_client(self):
        """Create the Groq client only when it is first needed."""
        if self.client is None:
            self.client = Groq(
                api_key=current_app.config["GROQ_API_KEY"]
            )
        return self.client

    def process_contract(self, contract_text):
        return self.extract_contract_info(contract_text)

    def extract_contract_info(self, contract_text):

        client = self._get_client()

        input_text = contract_text[:20000]

        prompt = f"""
Analyze the following legal contract and extract specific information.

Provide the output in exactly this format:

SUMMARY: [100-150 word summary covering purpose, obligations, and risks]
TERMINATION: [Extracted termination clause or 'Not found']
CONFIDENTIALITY: [Extracted confidentiality clause or 'Not found']
LIABILITY: [Extracted liability clause or 'Not found']

Contract Text:
{input_text}
"""

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional legal analyst."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,
            max_tokens=1024,
        )

        response = completion.choices[0].message.content

        return self.parse_llm_response(response)

    def parse_llm_response(self, text):

        data = {
            "summary": "",
            "termination": "",
            "confidentiality": "",
            "liability": ""
        }

        current_section = None

        for line in text.splitlines():

            line = line.strip()

            if not line:
                continue

            if line.upper().startswith("SUMMARY:"):
                current_section = "summary"
                data[current_section] = line.split(":", 1)[1].strip()

            elif line.upper().startswith("TERMINATION:"):
                current_section = "termination"
                data[current_section] = line.split(":", 1)[1].strip()

            elif line.upper().startswith("CONFIDENTIALITY:"):
                current_section = "confidentiality"
                data[current_section] = line.split(":", 1)[1].strip()

            elif line.upper().startswith("LIABILITY:"):
                current_section = "liability"
                data[current_section] = line.split(":", 1)[1].strip()

            elif current_section:
                data[current_section] += " " + line

        return data