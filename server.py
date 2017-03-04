from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/is_alive/', methods=['GET'])
def is_alive():
    return jsonify({'success':True})

@app.route('/', methods=['POST', 'GET'])
def messenger():
    content = request.get_json(silent=True)
    return jsonify(content)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
