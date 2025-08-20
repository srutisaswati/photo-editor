# 📸 Photo Editor (Streamlit App)

An interactive **photo editor web app** built with **Streamlit**.  
Easily apply filters, adjust brightness/contrast, resize, and add text overlays to your images — all inside a browser!

---

## 🚀 Features
- 📂 Upload any image (JPG, PNG, etc.)
- 🎨 Apply filters: grayscale, sepia, blur, sharpen, etc.
- ✂ Edit tools: resize, rotate, brightness/contrast
- 📝 Add text overlays to your image
- 🎭 Highlight & effects for creative editing
- 💾 Download your edited images
- 🤖 (Optional) Generate AI captions with Google Gemini

---

## 📦 Installation

Clone the repository and install dependencies:

bash
git clone https://github.com/your-username/photo-editor.git
cd photo-editor
pip install -r requirements.txt
`

---

## ▶ Run the App

bash
streamlit run app.py


Then open your browser at **[http://localhost:8501](http://localhost:8501)**

---

## ⚙ Project Structure


📂 photo-editor/
 ├── app.py             # Main Streamlit app
 ├── requirements.txt   # Dependencies
 └── README.md          # Project documentation


---

## 🔑 Environment Variables (Optional for AI features)

If you’re using **Google Gemini API** for caption generation, add your API key in `.streamlit/secrets.toml`:

toml
[general]
GEMINI_API_KEY = "your_api_key_here"


---

## 🛠 Tech Stack

* [Streamlit](https://streamlit.io/) – Web app framework
* [Pillow](https://pillow.readthedocs.io/) – Image editing
* [OpenCV](https://opencv.org/) – Computer vision filters
* [Google Gemini API](https://ai.google.dev/) (optional) – AI captions
* Python 3.9+

---

## 📷 Demo

👉 Add a screenshot or gif of your app here.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

---

## 📜 License

This project is licensed under the **MIT License**.



---
