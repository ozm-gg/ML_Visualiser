import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from typing import Dict
import os

# Конфигурация API
API_URL = os.getenv("API_URL", "http://:8000")

# Функция для взаимодействия с API
def analyze_text(text: str) -> Dict:
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json={"text": text},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Ошибка при обращении к API: {str(e)}")
        return None

# Кастомный CSS
def load_css():
    st.markdown("""
        <style>
            # /* Основной фон и градиент */
            # .stApp {
            #     background: linear-gradient(120deg, #f6f9fc 0%, #eef2f7 100%);
            # }
            
            /* Стилизация кнопок */
            .stButton>button {
                background: linear-gradient(90deg, #4776E6 0%, #8E54E9 100%);
                color: white;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: 600;
                border: none;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            }
            .stTitle {
                color: green;
            }
            
            /* Текстовая область */
            .stTextArea>div>div>textarea {
                border-radius: 10px;
                border: 2px solid #e0e6ed;
                padding: 15px;
            }

    
            /* Анимированный текст */
            @keyframes fadeIn {
                0% { opacity: 0; }
                100% { opacity: 1; }
            }
            .animated-text {
                animation: fadeIn 2s ease-in-out;
                font-size: 24px;
                color: #4CAF50;
                text-align: center;
                margin-bottom:  20px ;
            }
            
            /* Карточка результата */
            .result-card {
                background: white;
                padding: 25px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
                margin: 2rem 0;
                border-left: 5px solid #4776E6;
            }
            

        </style>
    """, unsafe_allow_html=True)

def create_visualization(result: Dict):
    df = pd.DataFrame({
        "Class": ["POSITIVE", "NEGATIVE"],
        "Probability": [
            result['score'] if result['label'] == 'POSITIVE' else 1 - result['score'],
            result['score'] if result['label'] == 'NEGATIVE' else 1 - result['score']
        ]
    })
    
    fig = px.bar(df, x="Class", y="Probability", color="Class",
                labels={"Probability": "Вероятность", "Class": "Класс"},
                text="Probability", height=400)
    
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=50, r=50, t=50, b=50),
        xaxis=dict(tickfont=dict(size=12, color='black')),
        yaxis=dict(range=[0, 1.2], tickfont=dict(size=12, color='black')),
        showlegend=False
    )
    return fig

# Интерфейс
def main():
    load_css()
    st.markdown("<h1 style='text-align: center;'>Анализ тональности текста</h1>", unsafe_allow_html=True)
    st.markdown('<div class="animated-text">Введите текст, чтобы определить его тональность.</div>', 
                unsafe_allow_html=True)

    text = st.text_area("текст", "Я люблю всех и вся", label_visibility="collapsed")

    if st.button("Анализировать", key="predict_button"):
        with st.spinner("Анализируем текст..."):
            result = analyze_text(text)
            
            if result:
                # Отображение результата
                st.markdown(f"""
                    <div class="result-card">
                        <h2 style="margin-top: 0; color: #000000;">Результат анализа</h2>
                        <p style="font-size: 18px; color: #4a5568;">
                            Тональность: <span style="font-weight: 600; color: #4776E6">{result['label']}</span><br>
                            Уверенность: <span style="font-weight: 600; color: #4776E6">{result['score']:.2f}</span>
                        </p>
                    </div>
                """, unsafe_allow_html=True)

                fig = create_visualization(result)
                st.plotly_chart(fig, use_container_width=True)

# Запуск приложения
if __name__ == "__main__":
    main()