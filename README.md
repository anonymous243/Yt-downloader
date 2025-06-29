# Yt-downloader

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python&logoColor=white&style=flat-square)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-%20web%20app-green?logo=flask&logoColor=white&style=flat-square)](https://flask.palletsprojects.com/)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE)

Yt-downloader is a simple, interactive web application for downloading YouTube videos and audio in various formats. Powered by Python and Flask, it provides a clean web interface for quick and easy downloads.

---

## 🚀 Features

- Simple web interface (HTML + Flask backend)
- Download YouTube videos in multiple resolutions
- Download audio-only (mp3/m4a) from YouTube links
- Batch download support
- No user data or history tracked

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/anonymous243/Yt-downloader.git
   cd Yt-downloader
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install ffmpeg**  
   Download from [ffmpeg.org](https://ffmpeg.org/download.html) and ensure it is available in your system PATH.

---

## 🛠️ Usage

1. **Start the Flask server**
   ```bash
   python app.py
   ```

2. **Open your browser and go to:**  
   [http://localhost:5000](http://localhost:5000)

3. **Paste a YouTube URL**, choose your download format, and click **Download**!

---

## 📁 Project Structure

```
Yt-downloader/
├── app.py               # Main Flask backend
├── requirements.txt     # Python dependencies
├── templates/
│   └── index.html       # Main HTML template
├── static/              # CSS and JS assets
├── downloads/           # Where downloaded files are saved
└── README.md
```

---

## ⚙️ Configuration

- **Port:** Change the default port in `app.py` if needed.
- **Download folder:** Output goes to `/downloads` by default.
- **Formats:** Supported via pytube; expand by editing backend code.

---

## 🧩 Dependencies

- [pytube](https://pytube.io/) (YouTube download engine)
- [Flask](https://flask.palletsprojects.com/) (web framework)
- [ffmpeg](https://ffmpeg.org/) (video/audio conversion)

Install all Python dependencies:
```bash
pip install -r requirements.txt
```

---

## 🤝 Contributing

Pull requests and issues are welcome!  
Please open an [issue](https://github.com/anonymous243/Yt-downloader/issues) or submit a PR for improvements.

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---

## ⚠️ Disclaimer

This project is for educational use only. Please comply with YouTube’s Terms of Service and all applicable copyright regulations.


---

**Happy downloading!**
