"""
from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for session tracking

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        choice = request.form.get("choice")
        session["attempts"] = 0

        if choice == "number":
            session["secret"] = random.randint(1, 100)
            session["mode"] = "number"
        elif choice == "alphabet":
            session["secret"] = chr(random.randint(65, 90))  # A-Z
            session["mode"] = "alphabet"

        return redirect(url_for("game"))

    return render_template("index.html")

@app.route("/game", methods=["GET", "POST"])
def game():
    message = ""
    if request.method == "POST":
        guess = request.form.get("guess")

        # Number mode
        if session["mode"] == "number":
            try:
                guess = int(guess)
                if guess < 1 or guess > 100:
                    message = "⚠️ Please enter a number between 1 and 100."
                else:
                    session["attempts"] += 1
                    if guess == session["secret"]:
                        message = f"🎉 Correct! You guessed it in {session['attempts']} attempts."
                        sound = "correct"
                    elif guess < session["secret"]:
                        message = "Too low!"
                        sound = "wrong"
                    else:
                        message = "Too high!"
                        sound = "wrong"
            except ValueError:
                message = "⚠️ Please enter a valid number!"

        # Alphabet mode
        elif session["mode"] == "alphabet":
            guess = guess.upper()
            if not guess.isalpha() or len(guess) != 1:
                message = "⚠️ Please enter a single letter (A–Z)."
            elif guess < "A" or guess > "Z":
                message = "⚠️ Please enter a letter between A and Z."
            else:
                session["attempts"] += 1
                secret = session["secret"]
                if guess == secret:
                    message = f"🎉 Correct! You guessed it in {session['attempts']} attempts."
                    sound = "correct"
                elif guess < secret:
                    message = "Too low in the alphabet!"
                    sound = "wrong"
                else:
                    message = "Too high in the alphabet!"
                    sound = "wrong"

    return render_template("game.html", mode=session.get("mode"), message=message)

if __name__ == "__main__":
    app.run(debug=True)
"""
from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        choice = request.form.get("choice")
        session["attempts"] = 0

        if choice == "number":
            session["secret"] = random.randint(1, 100)
            session["mode"] = "number"
        elif choice == "alphabet":
            session["secret"] = chr(random.randint(65, 90))  # A-Z
            session["mode"] = "alphabet"

        return redirect(url_for("game"))

    return render_template("index.html")

@app.route("/game", methods=["GET", "POST"])
def game():
    message = ""
    sound = ""  # default: no sound

    if request.method == "POST":
        guess = request.form.get("guess")

        if session["mode"] == "number":
            try:
                guess = int(guess)
                if guess < 1 or guess > 100:
                    message = "⚠️ Please enter a number between 1 and 100."
                    sound = "wrong"
                else:
                    session["attempts"] += 1
                    if guess == session["secret"]:
                        message = f"🎉 Correct! You guessed it in {session['attempts']} attempts."
                        sound = "correct"
                    elif guess < session["secret"]:
                        message = "Too low!"
                        sound = "wrong"
                    else:
                        message = "Too high!"
                        sound = "wrong"
            except ValueError:
                message = "⚠️ Please enter a valid number!"
                sound = "wrong"

        elif session["mode"] == "alphabet":
            guess = guess.upper()
            if not guess.isalpha() or len(guess) != 1:
                message = "⚠️ Please enter a single letter (A–Z)."
                sound = "wrong"
            else:
                session["attempts"] += 1
                secret = session["secret"]
                if guess == secret:
                    message = f"🎉 Correct! You guessed it in {session['attempts']} attempts."
                    sound = "correct"
                elif guess < secret:
                    message = "Too low in the alphabet!"
                    sound = "wrong"
                else:
                    message = "Too high in the alphabet!"
                    sound = "wrong"

    return render_template("game.html", mode=session.get("mode"), message=message, sound=sound)

if __name__ == "__main__":
    app.run(debug=True)