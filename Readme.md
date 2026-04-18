# 🌿 AI Crop Health Analyzer  
### Papaya Leaf Disease Detection using Deep Learning

---

## 🚀 Overview

AI Crop Health Analyzer is a deep learning-based web application that detects diseases in papaya leaves using image classification.

Users can:
- 📸 Upload an image
- 📷 Capture using camera
- 🤖 Ask AI for disease insights

The system predicts the disease and provides detailed information including symptoms and solutions.

---

## 🎯 Problem Statement

Farmers often struggle to identify plant diseases early, leading to:

- ❌ Reduced crop yield  
- ❌ Financial losses  
- ❌ Incorrect pesticide usage  

This project aims to provide a **fast, accessible, and AI-powered solution** for early disease detection.

---

## 🧠 Solution

We developed a system that:

- Uses a trained CNN model to classify leaf diseases  
- Provides real-time predictions  
- Gives actionable insights (symptoms + treatment)  
- Works on both desktop and mobile devices  

---

## ⚙️ Tech Stack

| Category | Technology |
|--------|-----------|
| Backend | Flask (Python) |
| AI Model | TensorFlow / Keras |
| Frontend | HTML, CSS, JavaScript |
| Image Processing | OpenCV / PIL |
| Deployment | Render |
| Version Control | Git & GitHub |

---

## 🧪 Features

- ✅ Image Upload Detection  
- ✅ Camera-Based Detection  
- ✅ Confidence Score Display  
- ✅ Disease Description & Solution  
- ✅ Offline AI Assistant (No API cost)  
- ✅ Responsive UI (Mobile Friendly)  

---

## 🧬 Model Details

- Image Size: 224 × 224  
- Classes:
  - Bacterial Blight  
  - Carica Insect Hole  
  - Yellow Necrotic Spots Holes  
  - Healthy  

- Confidence threshold used to improve reliability

---

## 📸 How It Works

1. User uploads or captures an image  
2. Image is preprocessed (resized & normalized)  
3. Model predicts disease  
4. Result + confidence displayed  
5. AI assistant provides additional guidance  

---

## ⚠️ Limitations

- Model trained on limited dataset  
- May misclassify non-leaf images  
- Performance depends on image quality  

---

## 🔮 Future Improvements

- Add **Not_Leaf detection**  
- Use larger datasets (Mendeley / PlantVillage)  
- Improve accuracy with MobileNetV2  
- Add multilingual support  
- Deploy mobile app version  

---

## 📂 Project Structure
Papaya-Disease-Detection/
│
├── app.py
├── papaya_model.h5
├── requirements.txt
├── Procfile
│
├── static/
├── templates/
│ └── index.html


---

## ▶️ Run Locally

```bash
git clone https://github.com/your-username/papaya-disease-detection.git
cd papaya-disease-detection

pip install -r requirements.txt
python app.py

## 🌍 Deployment

The application is deployed on the cloud using **Render**, making it accessible from anywhere via a web browser on both desktop and mobile devices.

🔗 Live Demo: *(Add your deployed link here after deployment)*

---

## 🙌 Acknowledgment

This project was developed as part of a **Final Year Project** in Computer Science and Engineering, focusing on applying deep learning techniques to solve real-world agricultural problems.

---

## 📌 Author

**Ayushman Singh**  
🎓 B.Tech – Computer Science & Engineering (Data Science)  
📍 India  

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub!