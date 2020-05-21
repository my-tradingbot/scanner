import requests
import json
from urllib.parse import urljoin
import urllib3


class BaseClient(object):

    def __init__(self, base_url, verify=False, ok_codes=(200, 201, 204), headers=None, auth=None):
        self._base_url = base_url
        self._verify = verify
        self._ok_codes = ok_codes
        self._headers = headers
        self._auth = auth
        self._session = requests.Session()

    def _http_request(self, method, url_suffix, full_url=None, headers=None,
                      auth=None, json_data=None, params=None, data=None, files=None,
                      timeout=10, resp_type='json', ok_codes=None, **kwargs):
        urllib3.disable_warnings()
        try:
            # Replace params if supplied
            address = full_url if full_url else urljoin(self._base_url, url_suffix)
            headers = headers if headers else self._headers
            auth = auth if auth else self._auth
            # Execute
            res = self._session.request(
                method,
                address,
                verify=self._verify,
                params=params,
                data=data,
                json=json_data,
                files=files,
                headers=headers,
                auth=auth,
                timeout=timeout,
                **kwargs
            )
            # Handle error responses gracefully
            if not self._is_status_code_valid(res, ok_codes):
                err_msg = 'Error in API call [{}] - {}' \
                    .format(res.status_code, res.reason)
                try:
                    # Try to parse json error response
                    error_entry = res.json()
                    err_msg += '\n{}'.format(json.dumps(error_entry))
                    raise ConnectionError(err_msg)
                except ValueError as exception:
                    raise (err_msg, exception)

            resp_type = resp_type.lower()
            try:
                if resp_type == 'json':
                    return res.json()
                if resp_type == 'text':
                    return res.text
                if resp_type == 'content':
                    return res.content
                return res
            except ValueError as exception:
                raise ('Failed to parse json object from response: {}'.format(res.content), exception)
        except requests.exceptions.ConnectTimeout as exception:
            err_msg = 'Connection Timeout Error - potential reasons might be that the Server URL parameter' \
                      ' is incorrect or that the Server is not accessible from your host.'
            raise (err_msg, exception)
        except requests.exceptions.SSLError as exception:
            err_msg = 'SSL Certificate Verification Failed - try selecting \'Trust any certificate\' checkbox in' \
                      ' the integration configuration.'
            raise (err_msg, exception)
        except requests.exceptions.ConnectionError as exception:
            # Get originating Exception in Exception chain
            error_class = str(exception.__class__)
            err_type = '<' + error_class[error_class.find('\'') + 1: error_class.rfind('\'')] + '>'
            err_msg = '\nError Type: {}\nError Number: [{}]\nMessage: {}\n' \
                      'Verify that the server URL parameter' \
                      ' is correct and that you have access to the server from your host.' \
                .format(err_type, exception.errno, exception.strerror)
            raise (err_msg, exception)

    def _is_status_code_valid(self, response, ok_codes=None):
        status_codes = ok_codes if ok_codes else self._ok_codes
        if status_codes:
            return response.status_code in status_codes
        return response.ok