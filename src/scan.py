import requests
import argparse

parser = argparse.ArgumentParser(description="Yahoo API Login Information")

parser.add_argument('-url', dest='url', help='API URL')
parser.add_argument('-token', dest='token', help='API Token Value')
parser.add_argument('-ticker', dest='ticker', help='Ticker To Query')

args = parser.parse_args()

if args.ticker is None:
  raise ValueError ("Ticker Symbol is Required")
elif args.url is None:
  raise ValueError ("API URL is Required")
elif args.token is None:
  raise ValueError ("API Token is Required")

get_qoutes_url = args.url + '/market/get-quotes'

params = {
  "region": "US",
  "lang": "en",
  "symbols": args.ticker
}

headers = {
  'X-RapidAPI-Key': args.token
}

response = requests.request("GET", get_qoutes_url, headers=headers, params=params)

print(response.text.encode('utf8'))
