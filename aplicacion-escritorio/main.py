# Importación de librerias
import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports


# Estado de conexión Bluetooth (por defecto 'Desconectado')
estado_bluetooth = "Desconectado"

# Función para actualizar el estado de conexión Bluetooth
def actualizar_estado_bluetooth(nuevo_estado):
    global estado_bluetooth
    estado_bluetooth = nuevo_estado
    label_estado.config(text=estado_bluetooth, fg="green" if estado_bluetooth == "Conectado" else "red")


# Establecer conexión serial
def conectar_bluetooth():
    global conexion_serial
    try:
        conexion_serial = serial.Serial("COM6", 9600)
        actualizar_estado_bluetooth("Conectado")
    except Exception as e:
        print("Error al conectar:", e)
        actualizar_estado_bluetooth("Error")


# Cierra la conexión serial
def desconectar_bluetooth():
    global conexion_serial
    if conexion_serial and conexion_serial.is_open:
        conexion_serial.close()
        actualizar_estado_bluetooth("Desconectado")


def estabilizar_camara():
    print("Estabilizando cámara...")


def tomar_foto():
    print("Tomando foto...")

def subir_facebook():
    print("Subiendo foto a Facebook...")

# Crear la ventana principal
app = tk.Tk()
app.title("Controlador de Cámara")
app.configure(bg='#0077be')  # Color de fondo estilo océano

# Establecer el icono de la ventana
ruta_icono = "./src/camera-icon.ico"  # Ruta al archivo de icono
app.iconbitmap(ruta_icono)

# Dimensiones de la ventana
ancho_ventana = 350
alto_ventana = 350

# Obtener dimensiones de la pantalla
ancho_pantalla = app.winfo_screenwidth()
alto_pantalla = app.winfo_screenheight()

# Calcular posición x, y
x = (ancho_pantalla // 2) - (ancho_ventana // 2)
y = (alto_pantalla // 2) - (alto_ventana // 2)
app.geometry(f'{ancho_ventana}x{alto_ventana}+{x}+{y}')  # Tamaño y posición de la ventana

# Crear un Frame para contener los botones y centrarlos
frame = tk.Frame(app, bg='#0077be')
frame.place(relx=0.5, rely=0.5, anchor='center')

# Estilo de los botones
style = ttk.Style()
style.configure('TButton', font=('Arial', 12))

# Crear y posicionar los botones dentro del Frame
boton_conectar = ttk.Button(frame, text="Conectar Bluetooth", command=conectar_bluetooth)
boton_conectar.pack(pady=10)

boton_estabilizar = ttk.Button(frame, text="Estabilizar Cámara", command=estabilizar_camara)
boton_estabilizar.pack(pady=10)

boton_tomar_foto = ttk.Button(frame, text="Tomar Foto", command=tomar_foto)
boton_tomar_foto.pack(pady=10)

boton_subir_facebook = ttk.Button(frame, text="Subir a Facebook", command=subir_facebook)
boton_subir_facebook.pack(pady=10)

# Crear un Label para mostrar el estado de conexión Bluetooth
label_estado = tk.Label(app, text=estado_bluetooth, fg="red", bg='#0077be', font=("Arial", 12))
label_estado.place(relx=0.9, rely=0.05, anchor='center')

# Crear y posicionar el botón Desconectar
boton_desconectar = ttk.Button(app, text="Desconectar", command=desconectar_bluetooth)
boton_desconectar.place(relx=0.8, rely=0.9, anchor='center')

# Iniciar el loop principal de la aplicación
app.mainloop()
