import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_groq(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=3000
    )
    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        parts = raw.split("```")
        raw = parts[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return raw.strip()


def generate_roadmap(topic):
    prompt = f"""
You are an expert learning roadmap generator.
Generate a detailed learning roadmap for: "{topic}"

Return ONLY a valid JSON object in this exact format:
{{
  "topic": "{topic}",
  "difficulty": "Beginner",
  "estimated_weeks": 8,
  "description": "Brief overview of this roadmap",
  "nodes": [
    {{
      "order": 1,
      "title": "Node Title",
      "description": "What you will learn in this step",
      "difficulty": "Beginner",
      "estimated_hours": 10,
      "resources": [
        {{
          "title": "Resource Name",
          "url": "https://example.com",
          "type": "video"
        }}
      ]
    }}
  ]
}}

Generate 8-12 nodes. Make resources real and accurate.
Return ONLY the JSON, no extra text, no markdown, no code blocks.
"""
    return json.loads(ask_groq(prompt))


def generate_quiz(topic, node_title):
    prompt = f"""
Generate 5 multiple choice questions about "{node_title}" in the context of {topic}.

Return ONLY a valid JSON array like this:
[
  {{
    "question": "Question text here?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "Option A",
    "explanation": "Brief explanation why this is correct"
  }}
]

Return ONLY the JSON array, no extra text, no markdown, no code blocks.
"""
    return json.loads(ask_groq(prompt))


def chat_with_advisor(roadmap_topic, user_message, history=[]):
    messages = [
        {
            "role": "system",
            "content": f"You are a helpful learning advisor for someone studying {roadmap_topic}. Give concise, practical advice."
        }
    ]
    for h in history:
        messages.append(h)
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message.content.strip()