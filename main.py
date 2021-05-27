from subprocess import (Popen, PIPE)
from re import match as re_match
from requests import (get, HTTPError)
from os import name as os_name
from os.path import (exists as path_exists, join as path_join)
from termcolor import colored


class GoogleChrome(object):

    _driver_repo_url = 'https://chromedriver.storage.googleapis.com/{version}/chromedriver_{os_name}{os_type}.zip'

    def __init__(self):
        self._version = '0.0'

    @property
    def operating_system_name(self) -> str: return 'win' if os_name == 'nt' else 'linux'

    @property
    def operating_system_type(self) -> str: return '64' if self.operating_system_name in ('mac', 'linux') else '32'

    @property
    def driver_repo_url(self) -> str: return self._driver_repo_url.format(
        version=self.version,
        os_name=self.operating_system_name,
        os_type=self.operating_system_type,
    )

    def download_driver(self) -> bool:
        print(self.driver_repo_url)
        filename = self.driver_repo_url.split('/')[-1]
        filename = filename.replace('.zip', f"_{self._version}.zip")
        try:
            response = get(self.driver_repo_url, timeout=30, stream=True)
            if response.status_code != 200:
                raise HTTPError(response.reason)
            with open(filename, 'wb') as fd:
                for chunk in response.iter_content(chunk_size=128):
                    fd.write(chunk)
        except Exception as error_message:
            message = str(error_message.args[0])
        finally:
            status = path_exists(filename)
            print(colored(
                text=f"File '{filename}'{' wasnt' if status is False else ''} downloaded",
                color='green' if status is True else 'red'
            ))
            return status

    @property
    def version(self) -> str:
        version = '0.0'
        try:
            p = Popen(f"google-chrome --version", stdout=PIPE, shell=True)
            output = str(p.communicate()[0].decode()).replace('\n', '').replace('\t', '').strip().split(' ')[-1]
            version = int(float(re_match(r"[0-9]{1,3}.[0-9]{1,3}", output).group(0)))
            if version == 2:
                self._version = '2.46'
            elif version == 73:
                self._version = '73.0.3683.68'
            elif version == 74:
                self._version = '74.0.3729.6'
            elif version == 75:
                self._version = '75.0.3770.140'
            elif version == 76:
                self._version = '76.0.3809.126'
            elif version == 77:
                self._version = '77.0.3865.40'
            elif version == 78:
                self._version = '78.0.3904.105'
            elif version == 79:
                self._version = '79.0.3945.36'
            elif version == 80:
                self._version = '80.0.3987.106'
            elif version == 81:
                self._version = '81.0.4044.138'
            elif version == 83:
                self._version = '83.0.4103.39'
            elif version == 84:
                self._version = '84.0.4147.30'
            elif version == 85:
                self._version = '85.0.4183.87'
            elif version == 86:
                self._version = '86.0.4240.22'
            elif version == 87:
                self._version = '87.0.4280.88'
            elif version == 88:
                self._version = '88.0.4324.96'
            elif version == 89:
                self._version = '89.0.4389.23'
            elif version == 90:
                self._version = '90.0.4430.24'
            elif version == 91:
                self._version = '91.0.4472.19'
        except Exception as error_message:
            print(f"Error getting Google-Chrome Version; {str(error_message.args[0])}")
        finally:
            return self._version


if __name__ == '__main__':
    g = GoogleChrome()
    print(f"Your Google Chrome version is {g.version}")
    g.download_driver()
