#!/usr/bin/env python3
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
from cachetools import cached, TTLCache
import urllib, urllib.parse
import json
import argparse
from threading import RLock

# In case of multi-threaded acceses: keep cache coherent
lock = RLock()

DEFAULT_BIND_ADDR = '127.0.0.1'
DEFAULT_PORT = 8332
CACHE_TIME = 5

# Totally decentralised!
BLOCKCHAIN_ENDPOINT = 'http://localhost:5000/lambda/'
def pass_through(method_name, arg=None):
    url = urllib.parse.urljoin(BLOCKCHAIN_ENDPOINT, method_name)
    if arg is not None:
        url = urllib.parse.urljoin(url + '/', str(arg))
    with urllib.request.urlopen(url) as s:
        return json.loads(s.read())

# JSON-RPC methods
@dispatcher.add_method
@cached(cache=TTLCache(maxsize=1, ttl=CACHE_TIME), lock=lock)
def getblockchaininfo():
    return pass_through('getblockchaininfo')

@dispatcher.add_method
@cached(cache=TTLCache(maxsize=1, ttl=CACHE_TIME), lock=lock)
def getmininginfo():
    return pass_through('getmininginfo')

@dispatcher.add_method
@cached(cache=TTLCache(maxsize=1, ttl=CACHE_TIME), lock=lock)
def getbalances():
    return pass_through('getbalances')

@dispatcher.add_method
@cached(cache=TTLCache(maxsize=1, ttl=CACHE_TIME), lock=lock)
def getbalance(id):
    return pass_through('getbalance', id)

# Daemon
@Request.application
def application(request):
    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='JSON-RPC daemon for the LambdaCoin blockchain.')
    parser.add_argument('-b', '--bind', default=DEFAULT_BIND_ADDR, help='bind on address')
    parser.add_argument('-p', '--port', default=DEFAULT_PORT, help='listen on port')

    args = parser.parse_args()
    try:
        args.port = int(args.port)
    except ValueError:
        parser.error("Port must be an integer.")

    run_simple(args.bind, args.port, application)
