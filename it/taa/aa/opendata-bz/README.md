## SETUP
1. Install Python: Ensure you have Python 3.9 installed. You can download it from the official Python website.
    
2. Create an env
   
    <code>pyenv virtualenv 3.9.7 opendata-bz</code>
    
    <code>pyenv activate opendata-bz</code>

4. Install Google Chrome: Download and install Google Chrome from the official website.

5. Install ChromeDriver: Download ChromeDriver from the official site. Ensure the version matches your Chrome version. Place the chromedriver executable in a directory included in your system's PATH or specify its location in your script.

6. Install required Python packages:
   
    <code>pip install --upgrade pip</code>
    
    <code>pip install -r requirements.txt</code>

## EXECUTE
> Run as **script** (setup CONFIG_FILE if different):

<code>pyenv activate opendata-bz && CONFIG_FILE=./etc/config/config.json && python3 ./src/download.py --configuration_file=$CONFIG_FILE --no-docker</code>

> ALTERNATIVE with **Docker**:
- build the image:

    <code>docker build -f ./Dockerfile -t opendata-bz:2.0 .</code>
- run the container (change CONFIG_FILE and OUTPUT_PATH accordingly)
  
    <code>CONFIG_FILE=./etc/config/config.json && OUTPUT_PATH=/media/lacie2022/data/meteo/eu/it/taa/aa/online/ && docker run --rm -v $CONFIG_FILE:/home/chromedriver/etc/conf/config.json -v $OUTPUT_PATH:/home/chromedriver/output/ opendata-bz:2.0</code>
