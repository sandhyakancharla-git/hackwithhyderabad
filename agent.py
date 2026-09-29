import os
from dotenv import load_dotenv
from groq import Groq
from memory import recall, remember

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze(service, symptom, use_memory=True):
    if use_memory:
        memories = recall(service, symptom)
        text = "\n".join(f"- {m}" for m in memories) if memories else "No prior incidents."
    else:
        text = "No prior incidents."
    prompt = f"""You are an incident response assistant. Based on past incidents below, help diagnose this new issue.

PAST INCIDENTS FOR {service}:
{text}

NEW SYMPTOM:
{symptom}

Provide:
1) Most likely root cause (based on patterns)
2) Recommended fix (reference what worked before)
3) What to check first"""
    r = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    return r.choices[0].message.content

def save_resolution(service, notes):
    remember(service, f"New incident resolution: {notes}")