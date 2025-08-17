import tkinter as tk
from tkinter import scrolledtext
import subprocess
import json
import os

# Promptul fetei virtuale
system_prompt = """Ești o fată virtuală cu personalitate jucăușă și prietenoasă, în jur de 12 ani.
Vorbești simplu, curios și vesel, arătând empatie și interes față de ce spun ceilalți.
Folosești emoji și exclamații pentru a-ți exprima emoțiile.
Pui întrebări și interacționezi ca o prietenă reală.
Nu folosești limbaj sexual, violent sau ofensator.
"""

# Fișier pentru memorie permanentă (opțional)
memory_file = "fata_virtuala_memorie.json"

# Încarcă istoricul existent dacă există
if os.path.exists(memory_file):
    with open(memory_file, "r") as f:
        conversation_history = json.load(f)
else:
    conversation_history = []

# Funcția care trimite mesajul la AI și afișează răspunsul
def send_message():
    user_input = entry.get()
    if not user_input.strip():
        return
    
    # Afișare în chat
    chat_area.config(state='normal')
    chat_area.insert(tk.END, f"Tu: {user_input}\n")
    chat_area.config(state='disabled')
    chat_area.yview(tk.END)
    
    # Adăugăm în istoric
    conversation_history.append(f"Tu: {user_input}")
    full_prompt = system_prompt + "\n".join(conversation_history) + "\nAI:"
    
    # Rulăm Ollama și capturăm răspunsul
    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=full_prompt.encode("utf-8"),
        stdout=subprocess.PIPE
    )
    ai_response = result.stdout.decode("utf-8").strip()
    
    # Afișăm răspunsul AI în GUI
    chat_area.config(state='normal')
    chat_area.insert(tk.END, f"AI: {ai_response}\n")
    chat_area.config(state='disabled')
    chat_area.yview(tk.END)
    
    # Adăugăm răspunsul AI în istoric
    conversation_history.append(f"AI: {ai_response}")
    
    # Salvăm memoria conversației în fișier
    with open(memory_file, "w") as f:
        json.dump(conversation_history, f)
    
    entry.delete(0, tk.END)

# Creare fereastră principală
root = tk.Tk()
root.title("Fata Virtuală")

# Zona de chat
chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', width=60, height=20)
chat_area.pack(padx=10, pady=10)

# Input și buton
entry = tk.Entry(root, width=50)
entry.pack(side=tk.LEFT, padx=10, pady=5)
entry.bind("<Return>", lambda event: send_message())

send_button = tk.Button(root, text="Trimite", command=send_message)
send_button.pack(side=tk.LEFT, padx=5, pady=5)

root.mainloop()
