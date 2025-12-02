import React, { useState } from 'react';
import GeometryViewer from './components/GeometryViewer';
import axios from 'axios'; // npm install axios

function App() {
  const [file, setFile] = useState(null);

  const handleUpload = async () => {
    if(!file) return;
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://localhost:8000/upload/geometry", formData);
      console.log("Upload Success:", res.data);
      alert("File uploaded to S3! Sim ID: " + res.data.sim_id);
    } catch (err) {
      console.error(err);
      alert("Upload Failed");
    }
  };

  return (
    <div className="App">
      {/* Overlay UI on top of the 3D Viewer */}
      <div style={{ position: 'absolute', zIndex: 10, padding: '20px', background: 'rgba(255,255,255,0.8)' }}>
        <h3>Physics AI v0.1</h3>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={handleUpload}>Upload CAD</button>
      </div>

      {/* The 3D Canvas */}
      <GeometryViewer />
    </div>
  );
}

export default App;
