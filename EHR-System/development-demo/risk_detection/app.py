from flask import jsonify, Flask

app = Flask(__name__)

@app.route("/")
def main_page():
    return "Main page", 200

@app.route("/health")
def health():
    return "OK", 200

@app.route("/calculate_risk", methods=['POST'])
def calculate_risk():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)