# disastereye
📌 Project Overview

DisasterEye is an AI-driven disaster recovery mapping system that utilizes OpenCV and machine learning models to analyze drone and satellite images of disaster-stricken areas. This system focuses on identifying and classifying infrastructure damage, debris, and regions requiring urgent attention, providing critical insights for disaster response teams.

📂 Dataset Information

Source: xView dataset

Structure:

Images: Pre- and post-disaster images (.png format)

Labels: JSON files containing metadata such as damage type, coordinates, and severity levels

Targets: Segmentation masks (_lab.png suffix) for training the AI model

![image](https://github.com/user-attachments/assets/e5ae6bbf-07f6-4e99-9470-a8f083e01f40)



🚀 Key Features

Pre- and Post-Disaster Image Analysis: Compares satellite images to detect changes and assess damage severity.

Damage Classification: Categorizes damage levels into superficial, medium, and major damage.

Automated Segmentation: Uses UNet-based segmentation and CNN models to extract disaster-affected regions.
![image](https://github.com/user-attachments/assets/484a9f4b-0d66-4a2f-b552-8805137052e2)
![image](https://github.com/user-attachments/assets/51c6ce35-f7e8-4302-80cf-82c3ab36c01b)
![image](https://github.com/user-attachments/assets/b0add8c9-de77-40e5-8815-12a421598f59)




YOLO-Based Victim Detection: Identifies and locates individuals trapped in disaster-stricken areas.

Prediction Models: Forecasts potential disaster impact using historical data and machine learning.
![image](https://github.com/user-attachments/assets/ff419f45-9efd-43ad-8e67-a33872d0fcfc)


Nowcast Warnings: Utilizes Google News (GNews) API for real-time disaster alerts and updates.

Chatbot Integration: Implements Gemini API to provide AI-driven disaster assistance.


⚙️ Technologies Used

Machine Learning & AI: OpenCV, UNet, YOLO, CNN, Gemini API

Data Processing: Python, Pandas, NumPy

Backend: Flask, Node.js

Frontend: Leaflet.js for interactive mapping


🔧 Installation & Setup

Clone the Repository

Install Dependencies: npm install

Run the Model:npm run dev

flask backend: python main.py

🤝 Contributions

We welcome contributions to improve DisasterEye! Feel free to fork the repo, make changes, and submit a pull request.
