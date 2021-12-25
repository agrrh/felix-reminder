FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY ./ ./

ENV PYTHONUNBUFFERED=yes
ENV PYTHONDONTWRITEBYTECODE=yes

ENTRYPOINT ["uvicorn"]
CMD ["main:app", "--host", "0.0.0.0", "--port", "8080"]
