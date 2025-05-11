# 🕵️ Image Steganography Web App

This is a Flask-based web application that allows users to **hide (encode)** and **extract (decode)** secret text messages inside images using **LSB (Least Significant Bit) steganography**.

## 🚀 Features

- Upload an image and hide a secret message
- Download the encoded image
- Upload an encoded image to decode the hidden message
- Simple and clean web interface

## 🔧 Technologies Used

- Python 3.x
- Flask
- OpenCV (cv2)
- Pillow
- HTML + CSS

## 📦 How to Run

```bash
# 1. Download Files 

# 2. Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install flask opencv-python pillow numpy

# 4. Run the app
python app.py
phy
