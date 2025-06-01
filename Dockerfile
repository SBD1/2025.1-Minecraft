FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*


COPY app/requirements.txt ./
RUN pip install --upgrade pip \
    && pip install -r requirements.txt


COPY . .

CMD ["python", "app.py"]
