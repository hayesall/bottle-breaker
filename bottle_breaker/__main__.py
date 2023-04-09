# Copyright © 2023 Alexander L. Hayes
# MIT License or Apache 2.0 License, at your choosing

import argparse

from bottle_breaker.app import app

PARSER = argparse.ArgumentParser()
PARSER.add_argument("-d", "--debug", action="store_true", help="Run in debug mode")

ARGS = PARSER.parse_args()

app.run(debug=ARGS.debug)
