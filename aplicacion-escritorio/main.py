import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports
import websockets
import asyncio
import requests
import threading

estado_bluetooth = "Desconectado"
websocket_server = "https://fr7pzf7n-3000.use2.devtunnels.ms/"  # Actualiza con la dirección correcta

def actualizar_estado_bluetooth(nuevo_estado):
    global estado_bluetooth
    estado_bluetooth = nuevo_estado
    label_estado.config(text=estado_bluetooth, fg="green" if estado_bluetooth == "Conectado" else "red")

async def enviar_caracter_a_react(caracter):
    async with websockets.connect(websocket_server) as websocket:
        await websocket.send(caracter)

def conectar_bluetooth():
    global conexion_serial
    try:
        conexion_serial = serial.Serial("COM10", 9600, timeout=1)
        conexion_serial.write(b'c')
        actualizar_estado_bluetooth("Conectado")
        print("Conectado")
    except Exception as e:
        print("Error al conectar:", e)
        actualizar_estado_bluetooth("Error")

def desconectar_bluetooth():
    global conexion_serial
    if conexion_serial and conexion_serial.is_open:
        conexion_serial.close()
        actualizar_estado_bluetooth("Desconectado")
        print("Desconectado")

def estabilizar_camara():
    global conexion_serial
    print("Estabilizando cámara...")
    if conexion_serial and conexion_serial.is_open:
        try:
            conexion_serial.write(b'a')
            print("Carácter 'a' enviado a Arduino")
        except Exception as e:
            print("Error al enviar a Arduino:", e)
    else:
        print("Bluetooth no está conectado")

def enviar_solicitud_capture_photo():
    url = 'https://fr7pzf7n-5000.use2.devtunnels.ms/capture_photo'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Solicitud enviada exitosamente:", response.json())
        else:
            print("Error en la solicitud:", response.status_code)
    except Exception as e:
        print("Error al realizar la solicitud:", e)

'''
Enviar a facebook
      const response = await fetch(
        "https://graph.facebook.com/v15.0/me/photos?access_token=EAAMeUmCcjUYBO9tAKCnFoBR8xs1BdQHRgvvNXCInnxyVZAFZCEhyTxDlTFAZAsvdUb1jcjZAL4reS7z4NQddYaZBVUjBkc8wZA2nlgtlxxIIUkycILC5KZBLHjbLNap5bbfbqfAcc38I8oEaO4fQX5o76tidkG8UQHzc1pv9ZC8TaKNPdQ3SX5358UXRmW1IvhHbZAoZBMku0ZD",
        {
          method: 'POST',
          body: formData,
        }
      );
'''

def enviar_foto_a_facebook():
    url_facebook = 


def ejecutar_asyncio_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_forever()

def correr_asyncio_coroutine(coroutine):
    asyncio.run_coroutine_threadsafe(coroutine, asyncio.get_event_loop())

def enviar_caracter_a_react_sincrono(caracter):
    correr_asyncio_coroutine(enviar_caracter_a_react(caracter))

def tomar_foto():
    global conexion_serial
    print("Tomando foto...")
    if conexion_serial and conexion_serial.is_open:
        try:
            conexion_serial.write(b'b')
            print("Carácter 'b' enviado a Arduino")
            enviar_solicitud_capture_photo()
            # Usar la función sincronizada para enviar el caracter a React
            enviar_caracter_a_react_sincrono('c')
        except Exception as e:
            print("Error al enviar a Arduino:", e)
    else:
        print("Bluetooth no está conectado")

def subir_facebook():
    print("Subiendo foto a Facebook...")

app = tk.Tk()
app.title("Controlador de Cámara")
app.configure(bg='#0077be')

# ruta_icono = "./src/camera-icon.ico"  # Descomenta y actualiza la ruta si tienes un ícono
# app.iconbitmap(ruta_icono)

ancho_ventana = 350
alto_ventana = 350

ancho_pantalla = app.winfo_screenwidth()
alto_pantalla = app.winfo_screenheight()

x = (ancho_pantalla // 2) - (ancho_ventana // 2)
y = (alto_pantalla // 2) - (alto_ventana // 2)
app.geometry(f'{ancho_ventana}x{alto_ventana}+{x}+{y}')

frame = tk.Frame(app, bg='#0077be')
frame.place(relx=0.5, rely=0.5, anchor='center')

style = ttk.Style()
style.configure('TButton', font=('Arial', 12))

boton_conectar = ttk.Button(frame, text="Conectar Bluetooth", command=conectar_bluetooth)
boton_conectar.pack(pady=10)

boton_estabilizar = ttk.Button(frame, text="Estabilizar Cámara", command=estabilizar_camara)
boton_estabilizar.pack(pady=10)

boton_tomar_foto = ttk.Button(frame, text="Tomar Foto", command=tomar_foto)
boton_tomar_foto.pack(pady=10)

boton_subir_facebook = ttk.Button(frame, text="Subir a Facebook", command=subir_facebook)
boton_subir_facebook.pack(pady=10)

label_estado = tk.Label(app, text=estado_bluetooth, fg="red", bg='#0077be', font=("Arial", 12))
label_estado.place(relx=0.9, rely=0.05, anchor='center')

boton_desconectar = ttk.Button(app, text="Desconectar", command=desconectar_bluetooth)
boton_desconectar.place(relx=0.8, rely=0.9, anchor='center')

# Iniciar el bucle de eventos de asyncio en un hilo separado
t = threading.Thread(target=ejecutar_asyncio_loop)
t.start()

app.mainloop()
