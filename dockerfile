FROM python:3.9

# Install Chrome & dependencies
RUN apt-get update && apt-get install -y \
    wget unzip curl \
    libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 \
    libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 \
    libxi6 libxtst6 x11-xserver-utils xvfb \
    && apt-get clean

# Install Chrome
RUN wget -qO- https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /usr/share/keyrings/google-chrome-keyring.gpg \
    && echo 'deb [signed-by=/usr/share/keyrings/google-chrome-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && apt-get clean

# Install ChromeDriver
RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip

# Set working directory
WORKDIR /app

# Copy script and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy script
COPY s3_bucket.py .

# Run script
CMD ["python", "s3_bucket.py"]
