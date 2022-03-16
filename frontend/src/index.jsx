import React, { useEffect, useRef, useState }  from "react";


const Classifier = () => {
    const canvasRef = useRef();
    const imageRef = useRef();
    const videoRef = useRef();

    const [result, setResult] = useState("");

    useEffect(() => {
        async function getCameraStream() {
            const stream = await navigator.mediaDevices.getUserMedia({
                audio: false,
                video: true
            });

            if (videoRef.current) {
                videoRef.current.srcObject = stream;
            }
        };

        getCameraStream();
        
    }, []);
    

    useEffect(() => {
        const interval = setInterval(async () => {
            await captureImageFromCamera();

            if(imageRef.current){
                const formData = new FormData();
                formData.append('image', imageRef.current);

                const response = await fetch('/classify', {
                    method: 'POST',
                    body: formData,
                });

                if (response.status === 200) {
                    const text = await response.text();
                    setResult(text);
                } else {
                    setResult("Error from API");
                }
            }
        }, 1000);

        return () => clearInterval(interval)
        
    }, []);
    
    const playCameraStream = () => {
        if (videoRef.current) {
            videoRef.current.play();
        }
    };

    const captureImageFromCamera = () => {
        const context = canvasRef.current.getContext('2d');
        const {videoWidth, videoHeight} = videoRef.current;

        canvasRef.current.width = videoWidth;
        canvasRef.current.height = videoHeight;

        context.drawImage(videoRef.current, 0, 0, videoWidth, videoHeight);
        canvasRef.current.toBlob((blob) => {
            imageRef.current = blob;
        })
    };
    

    return (
        <>
            <h1>Fashion Image Classifier</h1>
            <div>
                <video ref={videoRef} onCanPlay={() => playCameraStream()}/>
            </div>
            <div class="panel">
                <input id="file-upload" class="hidden" type="file" accept="image/x-png,image/gif,image/jpeg" />
                <label for="file-upload" id="file-drag" class="upload-box">
                <div id="upload-caption">Drop image here or click to select</div>
                <img id="image-preview" class="hidden" />
                </label>
            </div>
            <canvas ref={canvasRef} hidden></canvas>
            <p>Currently seeing: {result}</p>
        </>
    )
};

export default Classifier;