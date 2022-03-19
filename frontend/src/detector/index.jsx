import React, { useEffect, useRef, useState }  from "react";


const Detector = () => {
    const canvasRef = useRef();
    const imageRef = useRef();
    const videoRef = useRef();

    const [result, setResult] = useState("");

    useEffect(() => {
        async function getCameraStream() {
            const stream = await navigator.mediaDevices.getUserMedia({
                audio: false,
                video: {
                    width: {max: 320},
                    height: {max:240},
                    frameRate:{max:20,
                    ideal:15}
                }
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

                const response = await fetch('/detect', {
                    method: 'POST',
                    body: formData,
                });

                if (response.status === 200) {
                    const image_res = await response.blob();
                    const imageObjectURL = URL.createObjectURL(image_res);
                    setResult(imageObjectURL);
                    // console.log(imageObjectURL)
                    // console.log(image_res)
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
            <h1>Object Detector</h1>
            <div>
                <video ref={videoRef} onCanPlay={() => playCameraStream()}/>
            </div>
            
            <canvas ref={canvasRef} hidden></canvas>
            <div>
            <img alt="" src={result} width="320" />
            </div>
        </>
    )
};

export default Detector;