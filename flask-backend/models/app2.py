from flask import Flask, request, render_template_string
import torch
from PIL import Image
import numpy as np
import cv2
import tempfile
import os
import pathlib
import base64
import io

# Workaround for PosixPath error on Windows
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

# Load the YOLOv5 model
repo_path = r"C:\Users\Niharika Kashyap\Documents\jupyter[1]\yolov5"
model = torch.hub.load(repo_path, 'custom', path=r"C:\Users\Niharika Kashyap\Downloads\last.pt", source='local', force_reload=True)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file uploaded!"
        file = request.files['file']
        if file.filename == '':
            return "No file selected!"
        if file:
            file_type = file.content_type

            if file_type in ["image/jpeg", "image/png", "image/jpg"]:
                # Process image
                file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
                img = cv2.imdecode(file_bytes, 1)
                
                # Perform detection
                results = model(img)
                
                # Render bounding boxes directly on the image
                results.render()  # Draws boxes and labels directly on results.ims
                
                # Convert to RGB and encode as base64
                img_rgb = Image.fromarray(results.ims[0])  # results.ims holds the rendered image
                buffered = io.BytesIO()
                img_rgb.save(buffered, format="PNG")
                img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
                
                # Render the result in HTML
                return render_template_string('''
                    <h1>YOLOv5 Victim Detection App</h1>
                    <p>Upload an image or video to detect victims.</p>
                    <form method="POST" enctype="multipart/form-data">
                        <input type="file" name="file" accept=".jpg,.jpeg,.png,.mp4">
                        <button type="submit">Upload</button>
                    </form>
                    <h2>Detected Image:</h2>
                    <img src="data:image/png;base64,{{ img_base64 }}" alt="Detected Image" style="max-width: 100%;">
                    <br>
                    <a href="/">Upload another file</a>
                ''', img_base64=img_base64)

            elif file_type == "video/mp4":
                # Save uploaded video to a temporary file
                tfile = tempfile.NamedTemporaryFile(delete=False) 
                tfile.write(file.read())
                tfile.close()  # Close the file to release the handle
                
                # Open video file
                cap = cv2.VideoCapture(tfile.name)
                
                # Get video properties
                fps = cap.get(cv2.CAP_PROP_FPS)
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                
                # Output path for the processed video
                output_path = './static/output_video.mp4'  # Save in the static folder
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use mp4v for .mp4 format
                out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

                # Process each frame
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    # Perform detection
                    results = model(frame)
                    
                    # Render bounding boxes directly on the frame
                    results.render()  # Draws boxes and labels directly on results.ims
                    
                    # Convert BGR format for the output video writer
                    processed_frame = cv2.cvtColor(results.ims[0], cv2.COLOR_RGB2BGR)
                    out.write(processed_frame)

                # Release resources
                cap.release()
                out.release()
                
                # Clean up temporary files
                os.remove(tfile.name)
                
                # Render the result in HTML
                return render_template_string('''
                    <h1>YOLOv5 Victim Detection App</h1>
                    <p>Upload an image or video to detect victims.</p>
                    <form method="POST" enctype="multipart/form-data">
                        <input type="file" name="file" accept=".jpg,.jpeg,.png,.mp4">
                        <button type="submit">Upload</button>
                    </form>
                    <h2>Processed Video:</h2>
                    <video controls style="max-width: 100%;">
                        <source src="{{ url_for('static', filename='output_video.mp4') }}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                    <br>
                    <a href="/">Upload another file</a>
                ''')

    # Render the upload form for GET requests
    return render_template_string('''
        <h1>YOLOv5 Victim Detection App</h1>
        <p>Upload an image or video to detect victims.</p>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="file" accept=".jpg,.jpeg,.png,.mp4">
            <button type="submit">Upload</button>
        </form>
    ''')

if __name__ == '__main__':
    app.run(debug=True, port=5002)