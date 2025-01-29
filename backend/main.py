from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware

# Модель для входных данных
class TextInput(BaseModel):
    text: str

# Инициализация FastAPI
app = FastAPI()

# Добавляем CORS middleware для разрешения запросов от Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене заменить на конкретный URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создаем модель один раз при запуске сервера
model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Маршрут для предсказания
@app.post("/predict")
def predict(input: TextInput):
    try:
        result = model(input.text)[0]
        return {
            "label": result['label'],
            "score": result['score']
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Запуск: uvicorn main:app --reload