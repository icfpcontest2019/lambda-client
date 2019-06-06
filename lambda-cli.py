#!/usr/bin/env python3
from jsonrpc_requests import Server
import argparse

server = Server('http://localhost:8332')

if __name__ == '__main__':
    print(server.getblockchaininfo())
    print(server.getmininginfo())
    print(server.getbalances())
    print(server.getbalance(145))


