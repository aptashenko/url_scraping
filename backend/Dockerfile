FROM python:3.11-slim

# Установим системные зависимости
RUN apt-get update && apt-get install -y \
    wget curl gnupg ca-certificates fonts-liberation libasound2 libatk-bridge2.0-0 \
    libatk1.0-0 libcups2 libdbus-1-3 libdrm2 libexpat1 libgbm1 libglib2.0-0 \
    libgtk-3-0 libnspr4 libnss3 libx11-xcb1 libxcomposite1 libxdamage1 \
    libxext6 libxfixes3 libxrandr2 libxrender1 libxcb1 libxkbcommon0 \
    libxshmfence1 xdg-utils libgdk-pixbuf2.0-0 libatspi2.0-0 \
    libpangocairo-1.0-0 libpango-1.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Установка браузеров Playwright
RUN python3 -m playwright install --with-deps

COPY . .

CMD ["python3", "main.py"]