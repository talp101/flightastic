from flask import request, Response, Flask, jsonify

app = Flask(__name__)

@app.route('/is_alive/', methods=['GET'])
def is_alive():
    return jsonify({'success':True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
