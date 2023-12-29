import React, { useRef, useEffect } from "react";

import "./App.css";

function App() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      const constraints = { video: true };
      navigator.mediaDevices
        .getUserMedia(constraints)
        .then((stream) => {
          const video = videoRef.current;
          video.srcObject = stream;

          // Esperar a que los metadatos del video se carguen antes de reproducir
          video.onloadedmetadata = () => {
            video.play();
          };
        })
        .catch((err) => console.error("Error: " + err));
    }
  }, []);

  const capturePhoto = () => {
    const context = canvasRef.current.getContext("2d");
    context.drawImage(videoRef.current, 0, 0, 640, 480);

    // Crear un blob a partir del contenido del canvas
    canvasRef.current.toBlob((blob) => {
      const newImg = document.createElement("img");
      const url = URL.createObjectURL(blob);

      // Crear un elemento <a> para descargar la imagen
      const downloadLink = document.createElement("a");
      downloadLink.href = url;
      downloadLink.download = "captura.png"; // Nombre por defecto para la imagen

      // Simular un click para iniciar la descarga
      downloadLink.click();

      // Liberar el objeto URL después de la descarga
      URL.revokeObjectURL(url);
    }, "image/png");
  };

  return (
    <div>
      <video ref={videoRef} width="640" height="480" autoPlay />
      <button onClick={capturePhoto}>Capturar Foto</button>
      <canvas
        ref={canvasRef}
        width="640"
        height="480"
        style={{ display: "none" }}
      />
    </div>
  );
}

export default App;
