"""
ArdOmino CLI
"""

import argparse

def command_run(args):
    from . import app
    app.run(
        host=args.host,
        port=args.port,
        debug=args.debug)


def command_initdb(args):
    from ardomino import db
    db.create_all()


def get_argument_parser():
    parser = argparse.ArgumentParser(prog='ardomino')
    subparsers = parser.add_subparsers(help='sub-commands')

    parser_run = subparsers.add_parser('run')
    parser_run.add_argument('--debug', action='store_true', default=False)
    parser_run.add_argument('--host', default='0.0.0.0')
    parser_run.add_argument('--port', type=int, default=8080)
    parser_run.set_defaults(func=command_run)

    parser_initdb = subparsers.add_parser('initdb')
    parser_initdb.set_defaults(func=command_initdb)

    return parser


def run_from_command_line():
    parser = get_argument_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    run_from_command_line()
