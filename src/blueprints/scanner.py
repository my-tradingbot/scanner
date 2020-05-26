from flask import Blueprint, request
from flask import json
import alpaca_trade_api as alpacaapi

from .common import BaseClient

"""
    Create a new login session by setting environmental variables or using the login command
    $ export ALPACAURL="https://paper-api.alpaca.markets"
    $ export ALPACATOKENID="token-id"
    $ export ALPACATOKENSECRET="token-secret"
    or 
    python3 scan.py -l -url "https://paper-api.alpaca.markets" -keyid "yourkeyid" -keysecret "keysecret"
"""

BASE_URL = '/scan/'.strip('/')
scan = Blueprint('scanner', __name__)


class AlpacaClient(BaseClient):

    def query(self, suffix):
        res = self._http_request(
            method='Get',
            url_suffix=suffix
        )
        return res


@scan.route(f'/{BASE_URL}/test', methods=['GET'])
def test_api():
    try:
        test_request = json.loads(request.data.decode())

        if test_request.get('API') == 'alpaca':
            url = test_request.get('API-URL')
            headers = {
                "APCA-API-KEY-ID": test_request.get('API-TOKEN-ID'),
                "APCA-API-SECRET-KEY": test_request.get('API-TOKEN-SECRET')
            }
            try:
                client = AlpacaClient(
                    base_url=url,
                    verify=False,
                    headers=headers,
                    ok_codes=(200, 201, 204),
                )
            except Exception as e:
                raise (str(f'Failed to connect to the API. Error: {str(e)}'))

            return f"Alpaca API Test is Successful, Market TimeStamp:  {client.query('clock')['timestamp']}"
        else:
            return {
                'error': 'This API Request is not Currently Supported'
            }

    except ConnectionError as err_msg:
        raise ConnectionError(err_msg)


@scan.route(f'/{BASE_URL}/bars', methods=['GET'])
def get_bars():
    try:
        bars_request = json.loads(request.data.decode())

        if bars_request.get('API') == 'alpaca':
            url = bars_request.get('API-URL')
            headers = {
                "APCA-API-KEY-ID": bars_request.get('API-TOKEN-ID'),
                "APCA-API-SECRET-KEY": bars_request.get('API-TOKEN-SECRET')
            }
            try:
                client = AlpacaClient(
                    base_url=url,
                    verify=False,
                    headers=headers,
                    ok_codes=(200, 201, 204),
                )
            except Exception as e:
                raise (str(f'Failed to connect to the API. Error: {str(e)}'))

            query_symbols = bars_request['Query'].get('symbols')
            query_limit = bars_request['Query'].get('limit')
            query_start = bars_request['Query'].get('start')
            query_end = bars_request['Query'].get('end')
            query_after = bars_request['Query'].get('after')
            query_until = bars_request['Query'].get('until')
            query_timeframe = bars_request['Query'].get('timeframe')

            return client.query('bars/'+query_timeframe+'?'+'symbols='+query_symbols+'&'+'limit='+query_limit)
        else:
            return {
                'error': 'This API Request is not Currently Supported'
            }

    except ConnectionError as err_msg:
        raise ConnectionError(err_msg)


@scan.route(f'/{BASE_URL}/account/positions', methods=['GET'])
def get_account():
    try:
        get_account_request = json.loads(request.data.decode())

        if get_account_request.get('API') == 'alpaca':
            try:
                session = alpacaapi.REST(
                    base_url=get_account_request.get('API-URL'),
                    key_id=get_account_request.get('API-TOKEN-ID'),
                    secret_key=get_account_request.get('API-TOKEN-SECRET')
                )
                account = session.get_account()
                try:
                    return account.list_positions()
                except Exception as e:
                    raise ValueError('No Positions Opened')
                return 'test'
            except Exception as e:
                raise ConnectionError (str(f'Failed to connect to the API. Error: {str(e)}'))
        else:
            return {
                'error': 'This API Request is not Currently Supported'
            }


    except ConnectionError as err_msg:
        raise ConnectionError(err_msg)