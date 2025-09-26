
import requests
from flask import Flask, render_template, request
import markdown  # For pretty code/explanation display

API_KEY = "AIzaSyAts5SuLCYLZJn41Bdamsry_n2rm-hffgA"  # <-- Replace with your Gemini API key

def chat_with_muffin(prompt):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": API_KEY
    }
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        res = response.json()
        try:
            return res['candidates'][0]['content']['parts'][0]['text']
        except (KeyError, IndexError):
            return "Sorry, I couldn't understand the response from Gemini."
    else:
        return f"Error {response.status_code}: {response.text}"

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    answer_html = ""
    if request.method == "POST":
        user_input = request.form.get("user_input")
        if user_input:
            answer = chat_with_muffin(user_input)
            # Convert Markdown (with code blocks) to HTML for nice display
            answer_html = markdown.markdown(answer, extensions=['fenced_code'])
    return render_template("index.html", answer_html=answer_html)

if __name__ == "__main__":
    app.run(debug=True)