import React, { useState }  from "react";
import "./index.css"

const Detector = () => {
  
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState("");

  const onFileUpload = async (e) => {
    setLoading(true);
    setResult("");
    if (selectedFile){
      // console.log(selectedFile)
      const formData = new FormData();
      // formData.append("name", fileName);
      formData.append("image", selectedFile);


      const response = await fetch('/detect', {
        method: 'POST',
        body: formData,
      });
      
      if (response.status === 200) {
        setLoading(false);
        const img_res = await response.blob();
        const imgObjectURL = URL.createObjectURL(img_res);
        setResult(imgObjectURL);
      }
      else {
        console.log("Error from API")
        setResult("Error from API")
      }


    }
  }

  const handleImageInput = (e) => {
    const file = e.target.files[0];
    if (file){
      console.log(file);
      setSelectedFile(file)
    }
  }

  return(
    <>
    <h1>Object Detection</h1>
    <div>
      <input type="file" 
        accept="image/*"
        onChange={handleImageInput}
        />  
      <button
        onClick={(e)  => onFileUpload(e)}>Upload!</button>
    </div>

    {/* <span className="spinner" style={{display: loading ? "block" : "none"}}>
       Waiting...
    </span> */}

    <div className="lds-ellipsis" style={{display: loading ? "block" : "none"}}>
      <div></div><div></div><div></div><div></div></div>
    <div>
      
     <img src={result} alt="" width="320"/> 
    </div>
    
    </>
  )

};

export default Detector;