import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import subprocess

main_directory = os.path.join(sys.path[0])

def open_chrome_profile():
    subprocess.Popen(
        [
            'start',
            'chrome',
            '--remote-debugging-port=8989',
            '--user-data-dir=' + os.path.join(main_directory, 'chrome_profile')
        ],
        shell=True,
    )

open_chrome_profile()

def main():
    opt = Options()
    opt.add_experimental_option(name='debuggerAddress', value='localhost:8989')
    driver = webdriver.Chrome(options=opt)
    driver.get('https://unitsstorage.com/')

main()