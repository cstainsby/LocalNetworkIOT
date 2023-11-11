from flask import Flask

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return 'Hello from Python server!\n'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
