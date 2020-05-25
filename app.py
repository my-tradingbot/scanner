import argparse
from flask import Flask
from src.routes import configure_routes
app = Flask(__name__)
configure_routes(app)
print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Trading Listener Parameters")
    parser.add_argument('-host', dest='host', help='Listener IP')
    parser.add_argument('-port', dest='port', help='Listener IP')
    parser.add_argument('-debug', dest='debug', help='True to Enable Debug')
    args = parser.parse_args()
    app.run(host=args.host, port=args.port, debug=args.debug, ssl_context='adhoc')


