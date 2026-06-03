# Music Genre Predictor — Ажиллуулах заавар

---

## Mac дээр ажиллуулах

### 1. Python суулгасан эсэхийг шалгах
```bash
python3 --version
```
Python 3.8+ байвал болно. Байхгүй бол https://python.org -оос татаж суулгана.

### 2. Virtual environment үүсгэх
```bash
python3 -m venv venv
```

### 3. Virtual environment идэвхжүүлэх
```bash
source venv/bin/activate
```

### 4. Шаардлагатай сангуудыг суулгах
```bash
pip install -r requirements.txt
```

### 6. Апп ажиллуулах
```bash
streamlit run app.py
```

### 7. Хөтөч дээр нээх
Автоматаар нээгдэнэ. Нээгдэхгүй бол хөтөч дээр дараах хаягийг бичнэ:
```
http://localhost:8501
```

---

## Windows дээр ажиллуулах

### 1. Python суулгасан эсэхийг шалгах
```cmd
python --version
```
Python 3.8+ байвал болно. Байхгүй бол https://python.org -оос татаж суулгана.  
> Суулгахдаа **"Add Python to PATH"** сонголтыг заавал чагтална.

### 2. Virtual environment үүсгэх
```cmd
python -m venv venv
```

### 3. Virtual environment идэвхжүүлэх
```cmd
venv\Scripts\activate
```

### 4. Шаардлагатай сангуудыг суулгах
```cmd
pip install -r requirements.txt
```

### 6. Апп ажиллуулах
```cmd
streamlit run app.py
```

### 7. Хөтөч дээр нээх
Автоматаар нээгдэнэ. Нээгдэхгүй бол хөтөч дээр дараах хаягийг бичнэ:
```
http://localhost:8501
```

---

## Файлын бүтэц

```
genre_knn/
├── genre_knn.pkl       ← сургасан KNN загвар
├── app.py              ← Streamlit апп
├── requirements.txt    ← шаардлагатай сангуудын жагсаалт
└── steps_run.md        ← энэ файл
```

## Virtual environment-ийг дахин идэвхжүүлэх (дараа дахин ажиллуулахад)

**Mac:**
```bash
source venv/bin/activate
streamlit run app.py
```

**Windows:**
```cmd
venv\Scripts\activate
streamlit run app.py
```

## Зогсоох

Терминал дотор **Ctrl + C** дарна.

---

## Render дээр deploy хийх

### 1. GitHub репо үүсгэх
Кодоо GitHub дээр байршуулна (private эсвэл public аль ч болно).

### 2. `0.0.0.0` тохиргоо — ЗААВАЛ
Render дээр апп ажиллахын тулд Streamlit **`0.0.0.0`** хаягаар сонсох ёстой.  
Үүний тулд `.streamlit/config.toml` файл үүсгэж дараах агуулгыг бичнэ:

```
.streamlit/
└── config.toml
```

```toml
[server]
address = "0.0.0.0"
```

> ⚠️ Энэ тохиргоогүй бол Render дээр апп нээгдэхгүй — хандалт татгалзана.

### 3. Render дээр шинэ веб сервис үүсгэх
1. [render.com](https://render.com) руу нэвтрэх
2. **New → Web Service** дарах
3. GitHub репоо холбох
4. Дараах тохиргоог оруулах:

| Талбар | Утга |
|---|---|
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `streamlit run app.py --server.port $PORT --server.address 0.0.0.0` |

### 4. Deploy дарах
Render автоматаар код татаж, суулгаж, ажиллуулна.  
Амжилттай болвол `https://your-app-name.onrender.com` хаягаар нээгдэнэ.

### 5. Файлын бүтэц (deploy-д бэлэн)

```
genre_knn/
├── .streamlit/
│   └── config.toml     ← 0.0.0.0 тохиргоо
├── genre_knn.pkl
├── app.py
├── requirements.txt
├── .gitignore
└── steps_run.md
```
