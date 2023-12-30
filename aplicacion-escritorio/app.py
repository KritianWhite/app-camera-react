from flask import Flask, jsonify
from flask_socketio import SocketIO
import requests

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/capture_photo', methods=['GET'])
def capture_photo():
    socketio.emit('char', 'c')
    return jsonify(message='Carácter "c" enviado al frontend exitosamente')




def enviar_foto_a_facebook():
    url_facebook =  "https://graph.facebook.com/v15.0/me/photos?access_token=EAAMeUmCcjUYBO9tAKCnFoBR8xs1BdQHRgvvNXCInnxyVZAFZCEhyTxDlTFAZAsvdUb1jcjZAL4reS7z4NQddYaZBVUjBkc8wZA2nlgtlxxIIUkycILC5KZBLHjbLNap5bbfbqfAcc38I8oEaO4fQX5o76tidkG8UQHzc1pv9ZC8TaKNPdQ3SX5358UXRmW1IvhHbZAoZBMku0ZD"
    try:
        response = requests.get(url_facebook)
        if response.status_code == 200:
            print("Solicitud enviada exitosamente:", response.json())
        else:
            print("Error en la solicitud:", response.status_code)
    except Exception as e:
        print("Error al realizar la solicitud:", e)

if __name__ == '__main__':
    socketio.run(app, port=5000)
