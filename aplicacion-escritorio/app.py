from flask import Flask, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/capture_photo', methods=['GET'])
def capture_photo():
    socketio.emit('char', 'c')
    return jsonify(message='Carácter "c" enviado al frontend exitosamente')

if __name__ == '__main__':
    socketio.run(app, port=5000)
