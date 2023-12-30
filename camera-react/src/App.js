import React, { useRef, useEffect, useState } from "react";
import { io } from "socket.io-client";
import "./App.css";

function App() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [imagen, setImagen] = useState(null);
  

  useEffect(() => {
    const socket = io("https://fr7pzf7n-5000.use2.devtunnels.ms");

    socket.on("char", (data) => {
      if (data === 'c') {
        capturePhoto();
      }
    });

    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      const constraints = { video: true };
      navigator.mediaDevices
        .getUserMedia(constraints)
        .then((stream) => {
          const video = videoRef.current;
          video.srcObject = stream;
          video.onloadedmetadata = () => {
            video.play();
          };
        })
        .catch((err) => console.error("Error: " + err));
    }
  }, []);

  const capturePhoto = () => {
    
    if (canvasRef.current && videoRef.current) {
      const context = canvasRef.current.getContext("2d");
      context.drawImage(videoRef.current, 0, 0, 640, 480);

      canvasRef.current.toBlob((blob) => {
        const url = URL.createObjectURL(blob);
        setImagen(blob)
        const downloadLink = document.createElement("a");
        downloadLink.href = url;
        downloadLink.download = "captura.png";
        downloadLink.click();
        URL.revokeObjectURL(url);
      }, "image/png");
    }
  };

  const handlePublicarFoto = async () => {
    try {
      // Subir la foto a Facebook usando fetch
      const formData = new FormData();
      formData.append('source', imagen);

      const response = await fetch(
        "https://graph.facebook.com/v15.0/me/photos?access_token=EAAMeUmCcjUYBO9tAKCnFoBR8xs1BdQHRgvvNXCInnxyVZAFZCEhyTxDlTFAZAsvdUb1jcjZAL4reS7z4NQddYaZBVUjBkc8wZA2nlgtlxxIIUkycILC5KZBLHjbLNap5bbfbqfAcc38I8oEaO4fQX5o76tidkG8UQHzc1pv9ZC8TaKNPdQ3SX5358UXRmW1IvhHbZAoZBMku0ZD",
        {
          method: 'POST',
          body: formData,
        }
      );

      const responseData = await response.json();

      console.log('Foto publicada con éxito:', responseData);
    } catch (error) {
      console.error('Error al publicar la foto en Facebook:', error);
    }
  };

  return (
    <div>
      <video ref={videoRef} width="640" height="480" autoPlay />
      <button onClick={handlePublicarFoto}>Publicar en Facebook</button>
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
