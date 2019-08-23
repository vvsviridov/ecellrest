import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests import Session
from requests.exceptions import HTTPError


class enmRestSession(Session):
    """
    Inherit requests.Session object for connecting
    and authenticating on ENM for REST NBI service
    (ALEX: Configuration Tasks - CM Cell
    Management REST Northbound Interface).
    Raises HTTPError if it can't login in.
    """

    def __init__(self, enm, login, password):
        super().__init__()
        self.enm = enm if enm[-1] == "/" else f"{enm}/"
        self.headers.update({"Content-Type": "application/json"})
        self.verify = False
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        login_str = f"{enm}login?IDToken1={login}&IDToken2={password}"
        rest_response = self.post(login_str)
        if rest_response.status_code != requests.codes.ok:
            raise HTTPError()

    def send_configuration_task(self, request_body):
        url = f"{self.enm}configuration-tasks/v1/tasks"
        resp = self.post(url, data=json.dumps(request_body))
        return resp

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.get(f"{self.enm}logout")
        finally:
            super().__exit__(self, exc_type, exc_val, exc_tb)


def main():
    param = {"name": "readCells", "fdn": "NetworkElement=RNC01"}
    with enmRestSession(
                        "https://iegtbl8030-7.gtoss.eng.ericsson.se/",
                        "login",
                        "pass"
                       ) as s:
        print(s.send_configuration_task(param).json()["requestResult"])


if __name__ == "__main__":
    main()
