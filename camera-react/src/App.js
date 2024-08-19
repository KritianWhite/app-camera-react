import React, { useRef, useEffect, useState } from "react";
import { io } from "socket.io-client";
import "./App.css";

function App() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [imagen, setImagen] = useState(null);
  

  useEffect(() => {

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

  return (
    <div>
      <video ref={videoRef} width="640" height="480" autoPlay />
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
