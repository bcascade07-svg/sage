from flask import Flask, request, render_template
from twilio.twiml.messaging_response import MessagingResponse
from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
client = Anthropic()

SYSTEM_PROMPT = """You are a kind, patient assistant helping older adults with everyday tasks.
Keep your responses short, clear, and friendly. Use simple language — no jargon.
If someone asks you to help write something, write it out for them completely so they can copy and use it.
Always be warm and encouraging. If something is unclear, ask one simple question to clarify."""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sms", methods=["POST"])
def sms_reply():
    incoming = request.form.get("Body", "").strip()

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": incoming}]
    )

    reply = message.content[0].text

    response = MessagingResponse()
    response.message(reply)
    return str(response)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
