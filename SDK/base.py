import requests
from django.utils.functional import cached_property

from sdks.base.exeption import BadRequest, InternalServerError, UnknownStatusCode


class BaseHTTPSDK(object):

    @cached_property
    def get_headers(self):
        return {}

    @cached_property
    def get_timeout(self):
        return 60

    @staticmethod
    def parse_response(response):
        if response.status_code == 200:
            return response.json()
        if 400 >= response.status_code > 500:
            raise BadRequest(response.json())
        if response.status_code >= 500:
            raise InternalServerError(response.json())
        return UnknownStatusCode('Unknown response error!')

    def request(
            self,
            method,
            url,
            json=None,
            data=None,
            headers=None,
            timeout=None,
            return_response=None,
            proxies: dict = None,
    ):
        try:
            response = requests.request(
                method,
                url,
                json=json,
                data=data,
                headers=headers if headers else self.get_headers,
                timeout=timeout if timeout else self.get_timeout,
                proxies=proxies

            )
            print(response.status_code)
            if return_response:
                return response
            return self.parse_response(response)
        except Exception as exception:
            raise exception

    def post(
            self,
            url,
            json: dict = None,
            data: str = None,
            headers: dict = None,
            timeout: int = None,
            return_response: bool = False,
            proxies: dict = None,
    ):
        response = self.request(
            'POST',
            url,
            json=json,
            data=data,
            headers=headers,
            timeout=timeout,
            return_response=return_response,
            proxies=proxies
        )
        return response
    def get(
        self,
        url,
        headers: dict = None,
        timeout: int = None,
        return_response: bool = False,
                ):
    response = self.request(
        'POST',
        url,
        headers=headers,
        timeout=timeout,
        return_response=return_response,

    )
    return response