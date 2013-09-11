def run(*args, **kwargs):
    from . import app
    app.run(*args, **kwargs)


def run_from_command_line():
    import optparse
    parser = optparse.OptionParser()
    parser.add_option('--debug', action='store_true', dest='debug',
                      default=False)
    parser.add_option('--host', action='store', dest='host', default="0.0.0.0")
    parser.add_option('--port', action='store', dest='port', default="5000")
    opts, args = parser.parse_args()
    run(
        host=opts.host,
        port=int(opts.port),
        debug=opts.debug)


if __name__ == '__main__':
    run_from_command_line()
