1. Install Python: Ensure you have Python 3.9 installed. You can download it from the official Python website.

2. Create an env
    python3.9 -m venv myenv
    source myenv/bin/activate

3. Install Google Chrome: Download and install Google Chrome from the official website.

4. Install ChromeDriver: Download ChromeDriver from the official site. Ensure the version matches your Chrome version. Place the chromedriver executable in a directory included in your system's PATH or specify its location in your script.

5. Install required Python packages:
    pip install -r requirements.txt

6. Activate the virtual environment:
    python3.9 -m venv myenv
    source myenv/bin/activate

7. Install the required packages:
    pip install -r requirements.txt

8. Run the script:
    source /media/windows/projects/scripts/meteoaltoadige/myenv/bin/activate && python /media/windows/projects/scripts/meteoaltoadige/download.py /media/windows/projects/scripts/meteoaltoadige/ /media/windows/projects/scripts/meteoaltoadige/config.json