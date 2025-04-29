FROM python:3.11-slim

# 1) Install system dependencies and specific Google Chrome version
RUN apt-get update && apt-get install -y \
    wget curl gnupg2 ca-certificates \
    fonts-liberation libasound2 libatk1.0-0 libcups2 \
    libdbus-1-3 libgdk-pixbuf2.0-0 libnspr4 libnss3 \
    libx11-xcb1 libxcomposite1 libxrandr2 libxss1 \
    libxtst6 libgtk-3-0 xdg-utils \
  && wget -qO- https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" \
         > /etc/apt/sources.list.d/google-chrome.list \
  && apt-get update && apt-get install -y google-chrome-stable=135.0.7049.114-1 \
  && rm -rf /var/lib/apt/lists/*

# 2) Copy requirements.txt before performing any changes on it
WORKDIR /app
COPY requirements.txt .

# 3) Install Python dependencies (including chromedriver-binary)
RUN pip install --no-cache-dir -r requirements.txt

# 4) Copy application code
COPY . .

# 5) Expose port 8000 and run the application using Gunicorn
EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "--timeout", "120", "app:app"]


