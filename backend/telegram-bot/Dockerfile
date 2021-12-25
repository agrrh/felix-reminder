FROM python:3.8-alpine

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY ./ ./

ENV PYTHONUNBUFFERED=yes
ENV PYTHONDONTWRITEBYTECODE=yes

ENTRYPOINT ["python3"]
CMD ["main.py"]
