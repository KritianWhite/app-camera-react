import serial
import time

# Asegúrate de reemplazar esto con el nombre del puerto al que está conectado tu HC-05
bluetooth_port = "COM10"  # Esto puede variar dependiendo de tu sistema operativo y configuración

# Configura la conexión serial
bluetooth = serial.Serial(bluetooth_port, 9600)
print("Conexión establecida")

bluetooth.flushInput()

try:
    while True:
        bluetooth.write(b"A")  # Envía el carácter 'A' a Arduino
        time.sleep(0.5)  # Espera un poco para recibir la respuesta
        input_data = bluetooth.readline()
        print("Leído:", input_data.decode().strip())  # Muestra la respuesta de Arduino
except KeyboardInterrupt:
    bluetooth.close()
