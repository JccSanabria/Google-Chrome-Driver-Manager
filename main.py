from subprocess import (Popen, PIPE)
from re import match as re_match
from requests import (get, HTTPError)
from os import (name as os_name, rename)
from os.path import (exists as path_exists)
from termcolor import colored
from zipfile import ZipFile
from io import BytesIO


class ChromeDriver(object):

    def __init__(self):
        self.host: str = f'https://{self.object_name}.storage.googleapis.com'
        self.chrome_version: str = self.__get_chrome_version__
        self.download_filename: str = f"{self.object_name}_{self.operating_system_name}{self.operating_system_type}.zip"
        self.extracting_filename = self.download_filename.replace('.zip', f"_{self.chrome_version}.zip")
        self.driver_repo_url: str = f"{self.host}/{self.chrome_version}/{self.download_filename}"

    @property
    def object_name(self) -> str: return str(self.__class__.__name__).lower()

    @property
    def operating_system_name(self) -> str: return 'win' if os_name == 'nt' else 'linux'

    @property
    def operating_system_type(self) -> str: return '64' if self.operating_system_name in ('mac', 'linux') else '32'

    def download_driver(self) -> bool:
        print(self.driver_repo_url)
        try:
            response = get(self.driver_repo_url, timeout=30, stream=True)
            if response.status_code != 200:
                raise HTTPError(response.reason)
            with open(self.extracting_filename, 'wb') as fd:
                for chunk in response.iter_content(chunk_size=128):
                    fd.write(chunk)
        except Exception as error_message:
            print(colored(
                text=str(error_message.args[0]),
                color='red'
            ))
        finally:
            status = path_exists(self.extracting_filename)
            print(colored(
                text=f"File '{self.extracting_filename}'{' wasnt' if status is False else ''} downloaded",
                color='green' if status is True else 'red'
            ))
            return status

    def extract_file(self):
        message = f"Tried to extract file '{self.extracting_filename}'"
        try:
            if not path_exists(self.extracting_filename):
                raise FileExistsError
            with open(self.extracting_filename, 'rb+') as file:
                z = ZipFile(BytesIO(file.read()))
                z.extractall()
            if path_exists(self.object_name) is True:
                rename(self.object_name, f"{self.object_name}_{self.chrome_version}")
                print(colored(
                    text="Extraction successfully!",
                    color="green"
                ))
        except FileExistsError as error_message:
            print(colored(
                text=f"File '{self.extracting_filename}' doesnt exist; retrying download and extraction",
                color="magenta"
            ))
            self.download_driver()
            self.extract_file()
        except Exception as error_message:
            message = str(error_message.args[0])
        finally:
            return

    @property
    def __get_chrome_version__(self) -> str:
        version = '0.0'
        try:
            p = Popen(f"google-chrome --version", stdout=PIPE, shell=True)
            output = str(p.communicate()[0].decode()).replace('\n', '').replace('\t', '').strip().split(' ')[-1]
            version = int(float(re_match(r"[0-9]{1,3}.[0-9]{1,3}", output).group(0)))
            if version == 2:
                self._chrome_version = '2.46'
            elif version == 73:
                self._chrome_version = '73.0.3683.68'
            elif version == 74:
                self._chrome_version = '74.0.3729.6'
            elif version == 75:
                self._chrome_version = '75.0.3770.140'
            elif version == 76:
                self._chrome_version = '76.0.3809.126'
            elif version == 77:
                self._chrome_version = '77.0.3865.40'
            elif version == 78:
                self._chrome_version = '78.0.3904.105'
            elif version == 79:
                self._chrome_version = '79.0.3945.36'
            elif version == 80:
                self._chrome_version = '80.0.3987.106'
            elif version == 81:
                self._chrome_version = '81.0.4044.138'
            elif version == 83:
                self._chrome_version = '83.0.4103.39'
            elif version == 84:
                self._chrome_version = '84.0.4147.30'
            elif version == 85:
                self._chrome_version = '85.0.4183.87'
            elif version == 86:
                self._chrome_version = '86.0.4240.22'
            elif version == 87:
                self._chrome_version = '87.0.4280.88'
            elif version == 88:
                self._chrome_version = '88.0.4324.96'
            elif version == 89:
                self._chrome_version = '89.0.4389.23'
            elif version == 90:
                self._chrome_version = '90.0.4430.24'
            elif version == 91:
                self._chrome_version = '91.0.4472.19'
        except Exception as error_message:
            print(f"Error getting Google-Chrome Version; {str(error_message.args[0])}")
        finally:
            return self._chrome_version


if __name__ == '__main__':
    g = ChromeDriver()
    print(f"Your Google Chrome version is {g.chrome_version}")
    g.extract_file()
