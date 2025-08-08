FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app app/
COPY streamlit_app streamlit_app/

EXPOSE 8052
EXPOSE 8501

CMD uvicorn app.main:app --host 0.0.0.0 --port 8052 & streamlit run streamlit_app/dashboard.py --server.port 8501