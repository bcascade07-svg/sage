from flask import Flask, request, render_template
from twilio.twiml.messaging_response import MessagingResponse
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

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

    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        max_tokens=300,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": incoming}
        ]
    )

    reply = completion.choices[0].message.content

    response = MessagingResponse()
    response.message(reply)
    return str(response)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
