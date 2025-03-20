from flask import Flask, request, render_template_string
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
from matplotlib import cm
import io
import base64

app = Flask(__name__)

# Load the model
model = load_model(r"C:\Users\Niharika Kashyap\Pictures\satellite_segmentation_model.h5")

def preprocess_image(image):
    image_resized = cv2.resize(image, (256, 256)) / 255.0
    return np.expand_dims(image_resized, axis=0)

def predict_mask(image):
    preprocessed_image = preprocess_image(image)
    predicted_mask = model.predict(preprocessed_image)[0, :, :, 0]
    return predicted_mask

def plot_image_with_mask(original_image, mask):
    fig, ax = plt.subplots(1, 3, figsize=(18, 6))
    
    # Show the original image
    ax[0].imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
    ax[0].set_title("Original Image")
    ax[0].axis("off")
    
    # Show the predicted mask with a color map
    cax = ax[1].imshow(mask, cmap='jet')
    ax[1].set_title("Predicted Mask")
    ax[1].axis("off")
    
    # Add a color bar to represent intensity
    fig.colorbar(cax, ax=ax[1], orientation="vertical", fraction=0.046, pad=0.04)
    
    # Add a legend for color labels
    ax[2].axis("off")
    ax[2].text(0.5, 0.8, "Legend:", fontsize=14, ha='center', fontweight='bold')
    ax[2].text(0.5, 0.6, "Red/Yellow: Undamaged Area", color="Red", fontsize=12, ha='center')
    ax[2].text(0.5, 0.4, "Light Blue: Minor Damaged Area", color="blue", fontsize=12, ha='center')
    ax[2].text(0.5, 0.2, "Blue: Damaged Area", color="blue", fontsize=12, ha='center')
    
    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    
    # Encode the image to base64 for embedding in HTML
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return image_base64

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file uploaded!"
        file = request.files['file']
        if file.filename == '':
            return "No file selected!"
        if file:
            # Read the uploaded image
            image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), 1)
            
            # Make predictions
            mask = predict_mask(image)
            
            # Generate the plot and convert it to base64
            result_image = plot_image_with_mask(image, mask)
            
            # Render the result in HTML
            return render_template_string('''
                <h1>Satellite Image Segmentation</h1>
                <p>Upload a satellite image to see its segmentation mask with a heat bar and color labels.</p>
                <form method="POST" enctype="multipart/form-data">
                    <input type="file" name="file" accept=".png,.jpg,.jpeg">
                    <button type="submit">Upload</button>
                </form>
                <h2>Result:</h2>
                <img src="data:image/png;base64,{{ result_image }}" alt="Segmentation Result">
                <br>
                <a href="/">Upload another image</a>
            ''', result_image=result_image)
    
    # Render the upload form for GET requests
    return render_template_string('''
        <h1>Satellite Image Segmentation</h1>
        <p>Upload a satellite image to see its segmentation mask with a heat bar and color labels.</p>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="file" accept=".png,.jpg,.jpeg">
            <button type="submit">Upload</button>
        </form>
    ''')

if __name__ == '__main__':
    app.run(debug=True, port=5001)