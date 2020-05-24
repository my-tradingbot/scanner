import json

ALPACA_URL = 'https://paper-api.alpaca.markets'


def load_test_data(json_path):
    with open(json_path) as f:
        return json.load(f)


def test_server():
    import server
    import requests_mock

    with requests_mock.Mocker() as mock:
        alpaca_clock_response = load_test_data('./src/test_data/alpaca_clock.json')
        mock.get(f'{ALPACA_URL}/v2/clock', json=alpaca_clock_response)

    client = server.create_app(host='0.0.0.0',port='5000',debug=True)
    request=client.test_client()
    _, outputs, _ = request.get('/scan/test',json={
            "API": "alpaca",
            "API-URL": "https://paper-api.alpaca.markets",
            "API-TOKEN-ID": "tokenid",
            "API-TOKEN-SECRET": "tokensecret"
    })
    expected_output = 'Alpaca API Test is Successful, Market TimeStamp: 2020-05-24T13:25:41.850173499-04:00'

    assert expected_output == outputs

