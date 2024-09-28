from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello, World!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    # Here you would process the data (e.g., run a ML model)
    return jsonify({'prediction': 'sample prediction'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)

