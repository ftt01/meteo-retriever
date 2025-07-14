## SETUP
1. Install Python: Ensure you have Python 3.9 installed. You can download it from the official Python website.
    
2. Create an env
    pyenv virtualenv 3.9.7 opendata-bz
    pyenv activate opendata-bz

3. Install Google Chrome: Download and install Google Chrome from the official website.

4. Install ChromeDriver: Download ChromeDriver from the official site. Ensure the version matches your Chrome version. Place the chromedriver executable in a directory included in your system's PATH or specify its location in your script.

5. Install required Python packages:
    pip install --upgrade pip
    pip install -r requirements.txt

## EXECUTE
> Run the script (setup CONFIG_FILE if different):
    pyenv activate opendata-bz && CONFIG_FILE=./etc/config/config.json && python3 ./src/download.py --configuration_file=$CONFIG_FILE --no-docker

> ALTERNATIVE with Docker:

- build the image:
    docker build -f ./Dockerfile -t opendata-bz:2.0 .

- run the script (change CONFIG_FILE and OUTPUT_PATH accordingly)
    CONFIG_FILE=./etc/config/config.json && OUTPUT_PATH=/media/lacie2022/data/meteo/eu/it/taa/aa/online/ && docker run --rm -v $CONFIG_FILE:/home/chromedriver/etc/conf/config.json -v $OUTPUT_PATH:/home/chromedriver/output/ opendata-bz:2.0
