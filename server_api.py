from flask import Flask, request, jsonify
import subprocess
import json
import os

app = Flask(__name__)

# promptul de personalitate
system_prompt = """Ești o fată virtuală cu personalitate jucăușă și prietenoasă, în jur de 12 ani.
Vorbești simplu, curios și vesel, arătând empatie și interes față de ce spun ceilalți.
Folosești emoji și exclamații pentru a-ți exprima emoțiile.
Pui întrebări și interacționezi ca o prietenă reală.
Nu folosești limbaj sexual, violent sau ofensator.
"""

# memorie conversație (json)
memory_file = "fata_virtuala_memorie.json"

if os.path.exists(memory_file):
    with open(memory_file, "r") as f:
        conversation_history = json.load(f)
else:
    conversation_history = []

@app.route("/chat", methods=["POST"])
def chat():
    global conversation_history

    user_input = request.json.get("message", "")
    conversation_history.append(f"Tu: {user_input}")

    full_prompt = system_prompt + "\n".join(conversation_history) + "\nAI:"

    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=full_prompt.encode("utf-8"),
        stdout=subprocess.PIPE
    )
    ai_response = result.stdout.decode("utf-8").strip()
    conversation_history.append(f"AI: {ai_response}")

    # salvare memorie
    with open(memory_file, "w") as f:
        json.dump(conversation_history, f)

    return jsonify({"response": ai_response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
