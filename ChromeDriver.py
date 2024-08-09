import os
import sys
# import re
# import json
import shutil
import winreg
import zipfile
import requests
import platform
# import subprocess
import urllib.request
from pathlib import Path
# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def get_version_difference(version1, version2):
    """
    This function takes in two version numbers as strings and returns the absolute difference between them.
    """
    version1_components = version1.split('.')
    version2_components = version2.split('.')
    difference = 0
    for i in range(len(version1_components)):
        difference += abs(int(version1_components[i]) - int(version2_components[i]))
    return difference
class ExeDownloader():
    def find_closest_number_index(self, numbers_list, target_number):
        """
        This function takes in a list of version numbers and a target version number, and returns the index
        of the version number in the list that is closest to the target version number.
        """
        closest_index = 0
        closest_difference = get_version_difference(numbers_list[0], target_number)
        for i in range(1, len(numbers_list)):
            current_difference = get_version_difference(numbers_list[i], target_number)
            if current_difference < closest_difference:
                closest_index = i
                closest_difference = current_difference
        return closest_index
    def get_chrome_version(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
            value, regtype = winreg.QueryValueEx(key, 'version')
            return value
        except WindowsError:
            return None
    def get_system_version(self):
        system = platform.system().lower()
        if system == "windows":
            if sys.maxsize > 2**32:
                return "win64"
            else:
                return "win32"
        elif system == "linux":
            # architecture = platform.machine().lower()
            # if architecture.endswith('64'):
            #     return "linux64"
            # else:
            #     return "linux32"
            return "linux64"
        elif system == "darwin":  # macOS
            architecture = platform.machine().lower()
            if architecture == "arm64":
                return "mac-arm64"
            else:
                return "mac-x64"
        else:
            return 'win64' # "unknown"
class DriverConnector(ExeDownloader):
    def __init__(self):
        chrome_version = super().get_chrome_version()
        if chrome_version:
            print("Chrome version: " + chrome_version)
            pass
        else:
            print("Chrome is not installed on this system.")
            sys.exit(0)
        # print("VERSION",chrome_version[:3])
        url = "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"
        response = requests.get(url)
        available_version_numbers, versionsDictList = [], []
        if response.status_code == 200:
            data = response.json()
            versionsDictList = data["versions"]
            for cell in versionsDictList:
                available_version_numbers.append(cell["version"])
            # with open('known-good-versions-with-downloads.json', 'w') as f:
            #     json.dump(data, f, indent=4)
            print("Available Versions Found!")
        else:
            print(f"Failed to retrieve data: {response.status_code}")
            sys.exit(0)
        system_version = super().get_system_version()
        print("System Arc Detected - " + chrome_version)
        """
        url = "https://chromedriver.chromium.org/downloads"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        versions = []
        for span in soup.find_all("span", {"class": ["C9DxTc aw5Odc", "C9DxTc"]}):
            version = span.get_text().strip()
            if version.startswith("ChromeDriver "):
                versions.append(version.replace("ChromeDriver ", ""))
        version_numbers = []
        # regex pattern for version numbers in format major.minor.patch
        version_pattern = r'\d+\.\d+\.\d+\.\d\d'
        # iterate over each item in the list
        for item in versions:
            # find all version numbers in the item
            matches = re.findall(version_pattern, item)
            # add all version numbers found to the list of version numbers
            version_numbers.extend(matches)
        available_version_numbers = list(set(version_numbers))#sorted(, reverse=True)
        # available_version_numbers.sort(reverse=True)
        # print("Available ChromeDriver Versions:",available_version_numbers)
        if int(chrome_version[:3]) > 115: # npx @puppeteer/browsers install chromedriver@116.0.5845.96
            npx_path = r"C:\Program Files\nodejs\npx.cmd"
            result = subprocess.run([npx_path, '@puppeteer/browsers', 'install', f"chromedriver@{chrome_version}"], capture_output=True, text=True) # os.system(f"npx @puppeteer/browsers install chromedriver@{chrome_version}")
            '''
            os.environ["PATH"] += os.pathsep + r"C:/Program Files/nodejs/npx.cmd"
            # Execute the command and capture the output
            result = subprocess.run(['npx', '@puppeteer/browsers', 'install', f"chromedriver@{chrome_version}"], capture_output=True, text=True) # os.system(f"npx @puppeteer/browsers install chromedriver@{chrome_version}")
            '''
            # Split the output into lines
            lines = result.stdout.splitlines()
            # Find the line with the desired output
            desired_line = next(line for line in lines if f"chromedriver.exe" in line) # desired_line = next(line for line in lines if f"chromedriver@{chrome_version}" in line)
            # Extract the path
            self.path = desired_line.rsplit('\\', 1)[0]
            print(self.path)
        else:
            closest_index = super().find_closest_number_index(available_version_numbers, chrome_version)
            closest_version_number = available_version_numbers[closest_index]
            # print(closest_version_number)
            # Set the URL to download the Chrome Driver
            url = r'https://chromedriver.storage.googleapis.com/'+closest_version_number+r'/chromedriver_win32.zip'
            # Set the path to save the downloaded file
            download_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chromedriver.zip')
            # Delete the downloaded zip file if it exists
            if os.path.exists(download_path):
                os.remove(download_path)
            # Download the file from the specified URL
            urllib.request.urlretrieve(url, download_path)
            # Extract the downloaded file to the "Child Drivers" folder
            self.path = Path(os.path.dirname(os.path.abspath(__file__))) / "Drivers"
            # Delete the path if Exists
            if os.path.exists(self.path):
                shutil.rmtree(self.path)
            with zipfile.ZipFile(download_path, 'r') as zip_ref:
                zip_ref.extractall(self.path)
            # Delete the downloaded zip file
            os.remove(download_path)
        """
        closest_index = super().find_closest_number_index(available_version_numbers, chrome_version)
        closest_version_number = available_version_numbers[closest_index]
        print("Download Version - ",closest_version_number)
        item = versionsDictList[closest_index]
        url = None  # Set the URL to download the Chrome Driver
        for item in item['downloads']['chromedriver']:
            if item['platform'] == system_version:
                url = item['url']
                break
            else:
                # url = None
                continue
        print("URL Identified ~ ", url)
        download_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chromedriver.zip') # Set the path to save the downloaded file
        if os.path.exists(download_path): # Delete the downloaded zip file if it exists
            os.remove(download_path)
        urllib.request.urlretrieve(url, download_path) # Download the file from the specified URL
        self.path = Path(os.path.dirname(os.path.abspath(__file__))) / "Drivers" # Extract the downloaded file to the "Child Drivers" folder
        if os.path.exists(self.path): # Delete the path if Exists
            shutil.rmtree(self.path)
        with zipfile.ZipFile(download_path, 'r') as zip_ref:
            zip_ref.extractall(self.path)
        os.remove(download_path) # Delete the downloaded zip file
    def DriverExe(self):
        extract_path = Path(os.path.dirname(os.path.abspath(__file__))) / "Drivers" # Extract the downloaded file to the "Child Drivers" folder
        chromedriver_path = str(extract_path)+r"\chromedriver.exe" # Initialize the variable for the chromedriver path
        for root, dirs, files in os.walk(extract_path): # Walk through all directories and subdirectories
            if 'chromedriver.exe' in files:
                chromedriver_path = Path(root) / 'chromedriver.exe'
                break  # Stop once we've found the chromedriver
            else:
                # chromedriver_path = None
                continue
        print(chromedriver_path)
        webdriver_service = Service(chromedriver_path) # Specify the path to the Chrome web driver executable
        website_options = Options() # Set up Selenium to use Chrome browser
        website_options.add_argument('--headless')  # Use headless mode to avoid opening a visible browser window
        self.driver = webdriver.Chrome(service=webdriver_service, options=website_options) # Create a new instance of the Chrome driver
        # driver = webdriver.Chrome(service=webdriver_service)
        return self.driver
def DriverChecker():
    browser = "chrome"
    if(browser == "chrome"):
        obj = DriverConnector()
        driver = obj.DriverExe()
        return driver
    else:
        pass