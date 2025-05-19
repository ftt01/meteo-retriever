FROM python:3.9

# ADD /app/main.py .
# ADD /app/connectdriver.py .

# Install Chrome WebDriver
COPY resources/chromedriver_linux64.zip /opt/chromedriver_linux64.zip
RUN CHROMEDRIVER_VERSION=114.0.5735.90 && \
    mkdir -p /opt/chromedriver-$CHROMEDRIVER_VERSION && \
    unzip -qq /opt/chromedriver_linux64.zip -d /opt/chromedriver-$CHROMEDRIVER_VERSION && \
    rm /opt/chromedriver_linux64.zip && \
    chmod +x /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver && \
    ln -fs /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver /usr/local/bin/chromedriver

# RUN CHROMEDRIVER_VERSION=114.0.5735.90 && \
#     mkdir -p /opt/chromedriver-$CHROMEDRIVER_VERSION && \
#     curl -sS -o /tmp/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip && \
#     unzip -qq /tmp/chromedriver_linux64.zip -d /opt/chromedriver-$CHROMEDRIVER_VERSION && \
#     rm /tmp/chromedriver_linux64.zip && \
#     chmod +x /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver && \
#     ln -fs /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver /usr/local/bin/chromedriver

# Install Google Chrome
COPY resources/google-chrome-stable_114.0.5735.90-1_amd64.deb ./src/chrome_114_amd64.deb
RUN apt-get -yqq update && \
    apt-get -yqq upgrade && \
    apt-get -yqq install ./src/chrome_114_amd64.deb

RUN python -m pip install --upgrade pip

COPY requirements.txt .
RUN pip3 install -r requirements.txt

# RUN mkdir -p /home/chromedriver/test/
WORKDIR /home/chromedriver/

COPY etc/config/config.json /home/chromedriver/etc/conf/config.json
COPY src/download.py /home/chromedriver/src/download.py

# python /home/chromedriver/src/bin/download.py /home/chromedriver/ /home/chromedriver/etc/conf/config.json
# CMD ["python", "/home/chromedriver/src/bin/download.py", "/home/chromedriver/", "/home/chromedriver/etc/conf/config.json"]
CMD ["python", "/home/chromedriver/src/download.py"]