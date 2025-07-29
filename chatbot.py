from flask import Flask, request, jsonify, send_file
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)
FILE_NAME = "leads.xlsx"

# Save lead info (not yet used by UI but ready)
def save_lead(name, phone, email, description):
    data = {
        "Date": [datetime.now().strftime("%Y-%m-%d %H:%M")],
        "Name": [name],
        "Phone": [phone],
        "Email": [email],
        "Project Description": [description]
    }

    df = pd.DataFrame(data)

    if os.path.exists(FILE_NAME):
        existing = pd.read_excel(FILE_NAME)
        updated = pd.concat([existing, df], ignore_index=True)
    else:
        updated = df

    updated.to_excel(FILE_NAME, index=False)

# Basic response logic
def get_response(message):
    msg = message.lower()

    if "quote" in msg or "price" in msg:
        return "Please provide your name, phone, email, and a brief project description so we can prepare a quote."
    elif "inspection" in msg:
        return "We can schedule a roof inspection. Please provide your name, contact details, address, and preferred date."
    elif "emergency" in msg:
        return "For emergencies, please call us 24/7 at (800) 555-ROOF."
    elif "services" in msg:
        return "We offer roof installation, repairs, inspections, gutter services, and storm damage restoration."
    elif "contact" in msg:
        return "You can reach us at support@roofguardsolutions.com or call (800) 555-ROOF."
    else:
        return "I'm here to help with quotes, inspections, and roof repairs. How can I assist you?"

@app.route("/")
def index():
    # Serve index.html from same directory
    return send_file("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    reply = get_response(user_input)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)