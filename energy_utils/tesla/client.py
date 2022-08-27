import base64
import hashlib
import os
import time
from pprint import pprint
import secrets
import requests


class Client:
    base_url = "https://owner-api.teslamotors.com/api/1"
    auth_url = "https://auth.tesla.com/oauth2/v3/token"
    __headers = {"Content-Type": "application/json", "X-Tesla-User-Agent": "TeslaCharger/v0.1.1"}

    def __init__(self, auth_token, refresh_token, expiry):
        self.__expiry = expiry
        self.__refresh_token = refresh_token.strip()
        self.__auth_token = auth_token
        assert not self.is_expired()
        self.__headers["authorization"] = f"Bearer {auth_token}".strip()
        self.vehicles = self.__vehicles()

    def is_expired(self):
        return self.__expiry < time.time()

    def should_refresh_token(self):
        return self.__expiry < time.time() - 300  # If less than 300 valid sec left.

    def start_charging(self, vehicle_id: int):
        return self.post(url=self.base_url + f"/vehicles/{vehicle_id}/command/charge_start")["response"]["result"]

    def charge_state(self, vehicle_id: int):
        return self.get(url=self.base_url + f"/vehicles/{vehicle_id}/data_request/charge_state")

    def stop_charging(self, vehicle_id: int, safe=True):
        resp = requests.post(url=self.base_url + f"/vehicles/{vehicle_id}/command/charge_stop",
                             headers=self.__headers)
        if resp.status_code == 200:
            return resp.json()
        elif safe:
            self.start_charging(vehicle_id)
            return self.stop_charging(vehicle_id, False)
        else:
            raise resp.raise_for_status()

    def set_charge_limit(self, vehicle_id: int, limit: int):
        return self.post(self.base_url + f"/vehicles/{vehicle_id}/command/set_charge_limit?percent={limit}")

    def __vehicles(self):
        json = self.get(url=self.base_url + "/vehicles")
        return {k: v for k, v in [(v["id"], v['display_name']) for v in json["response"]]}

    @staticmethod
    def create_auth_url():
        # https://tesla-info.com/tesla-token.php
        # https://tesla-api.timdorr.com/api-basics/authentication#get-https-auth.tesla.com-oauth2-v3-authorize
        state = secrets.token_hex(16)

        verifier_bytes = os.urandom(128)[:86]
        code_verifier = base64.urlsafe_b64encode(verifier_bytes).rstrip(b"=")
        challenge_bytes = hashlib.sha256(code_verifier).digest()
        challenge = base64.urlsafe_b64encode(challenge_bytes).rstrip(b"=").decode("utf-8")
        url = f"https://auth.tesla.com/oauth2/v3/authorize?client_id=ownerapi&code_challenge={str(challenge)}&code_challenge_method=S256&redirect_uri=https%3A%2F%2Fauth.tesla.com%2Fvoid%2Fcallback&response_type=code&scope=openid+email+offline_access&state={state}"
        return url, code_verifier.decode("utf-8")

    @staticmethod
    def get_auth_token_from_url(url, code_verifier):
        code = url.split("code=")[-1].split("&")[0]
        return Client.get_auth_token_from_code(code, code_verifier)

    @staticmethod
    def get_auth_token_from_code(code, code_verifier):

        req = requests.post(url=Client.auth_url,
                            json={"grant_type": "authorization_code", "code": code,
                                  "client_id": "ownerapi", "code_verifier": code_verifier,
                                  "redirect_uri": "https://auth.tesla.com/void/callback"},
                            headers=Client.__headers)
        if req.status_code == 200:
            j = req.json()
            return j["access_token"], j["refresh_token"], \
                   int(j["expires_in"]) + int(time.time()) - 20  # Remove 20s to be safeish
        else:
            return req.raise_for_status()

    def start_hvac(self, vehicle_id):
        return self.post(Client.base_url + f"/vehicles/{int(vehicle_id)}/command/auto_conditioning_start")

    def post(self, url, json=None):
        print("POST " + url)
        if json is None:
            req = requests.post(url=url, headers=self.__headers)
        else:
            req = requests.post(url=url, headers=self.__headers, json=json)
        if req.status_code == 200:
            j = req.json()
            pprint(j)
            return j
        else:
            return req.raise_for_status()

    def get(self, url):
        print("GET " + url)
        req = requests.get(url=url, headers=self.__headers)

        if req.status_code == 200:
            j = req.json()
            pprint(j)
            return j
        else:
            return req.raise_for_status()

    def refresh_token(self):
        toks = self.post(url=Client.auth_url, json={"grant_type": "refresh_token", "client_id": "ownerapi",
                                                    "refresh_token": self.__refresh_token,
                                                    "scope": "openid email offline_access"})
        tok, refresh_tok, exp = toks["access_token"],\
                                toks["refresh_token"],\
                                int(toks["expires_in"]) + int(time.time()) - 20
        self.__headers["authorization"] = f"Bearer {tok}".strip()

        return tok, refresh_tok, exp