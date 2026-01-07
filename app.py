from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello world!"

@app.route('/none')
def none():
    return "Nothing to see here."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)