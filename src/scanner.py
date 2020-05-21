import argparse
import os
import alpaca_trade_api as tradeapi

from common import BaseClient

"""
    Create a new login session by setting environmental variables or using the login command
    $ export ALPACAURL="https://paper-api.alpaca.markets"
    $ export ALPACATOKENID="token-id"
    $ export ALPACATOKENSECRET="token-secret"
    or 
    python3 scan.py -l -url "https://paper-api.alpaca.markets" -keyid "yourkeyid" -keysecret "keysecret"
"""


class Client(BaseClient):

    def query(self, suffix):
        res = self._http_request(
            method='Get',
            url_suffix='/v2/'+suffix
        )
        return res


def test_api(client):
    try:
        market_clock = client.query('clock')
        return 'Test is Successful'
    except ConnectionError as err_msg:
        raise ConnectionError(err_msg)


def main():

    parser = argparse.ArgumentParser(description="ALPACA API Login Session Parameters")
    parser.add_argument('-url', dest='url', help='API URL')
    parser.add_argument('-tokenid', dest='tokenid', help='API Token ID')
    parser.add_argument('-tokensecret', dest='tokensecret', help='API Token Secret')
    args = parser.parse_args()


    try:
        url = os.environ["ALPACAURL"]
        token_id = os.environ["ALPACATOKENID"]
        token_secret = os.environ["ALPACATOKENSECRET"]
    except:
        raise ValueError("No enviromental variables configured, please rerun the scanner with API credentials")

    if args.url and args.tokenid and args.tokensecret:
        url, token_id, token_secret = args.url,args.tokenid,args.tokensecret


    headers = {
        "APCA-API-KEY-ID": token_id,
        "APCA-API-SECRET-KEY": token_secret
    }

    try:
        client = Client(
            base_url=url,
            verify=False,
            headers=headers,
            ok_codes=(200, 201, 204),
        )
    except Exception as e:
        raise (str(f'Failed to execute your command. Error: {str(e)}'))

    print(test_api(client))


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()

