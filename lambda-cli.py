#!/usr/bin/env python3
from jsonrpc_requests import Server
import argparse

DEFAULT_BIND_ADDR = '127.0.0.1'
DEFAULT_PORT = 8332

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Command-line interface for the LambdaCoin daemon.')
    parser.add_argument('-b', '--bind', default=DEFAULT_BIND_ADDR, help='daemon address')
    parser.add_argument('-p', '--port', default=DEFAULT_PORT, help='daemon port')
    subparsers = parser.add_subparsers(dest='subcmd', help='sub-command help')

    parser_bi = subparsers.add_parser('getblockchaininfo')
    parser_bi.add_argument('item', nargs='?', default=None, help="return key 'item' of result")

    parser_mi = subparsers.add_parser('getmininginfo')
    parser_bs = subparsers.add_parser('getbalances')

    args = parser.parse_args()
    try:
        args.port = int(args.port)
    except ValueError:
        parser.error('Port must be an integer.')

    server = Server(f'http://{args.bind}:{args.port}')

    if args.subcmd == 'getblockchaininfo':
        bi = server.getblockchaininfo()
        if args.item is None:
            print(bi)
        else:
            print(bi[args.item])

    elif args.subcmd == 'getmininginfo':
        print(server.getmininginfo())
    elif args.subcmd == 'getbalances':
        print(server.getbalances())


    # print(server.getblockchaininfo())
    # print(server.getmininginfo())
    # print(server.getbalances())
    # print(server.getbalance(145))


