import logging
import os
from argparse import ArgumentParser

import uvicorn
from dotenv import load_dotenv
from utils.evaluate import evaluate_cv


def cli_parser() -> ArgumentParser:
    """Builds an ArgumentParser to handle different commands.

    Returns:
        argparse.ArgumentParser: The parser.
    """
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    # run
    parser_run = subparsers.add_parser("run", help="runs the api")
    # eval
    parser_eval = subparsers.add_parser("eval", help="evaluates the cv model")
    parser_eval.add_argument("net", help="name of model to evaluate")
    parser_eval.add_argument(
        "-t",
        "--train",
        help="flag to train the model before evaluating",
        action="store_true",
    )

    return parser


def run():
    """Runs the backend api server. Will either run in development, staging, or
    production mode depending on the `env` environmental variable."""
    env = os.environ.get("env", "prod")
    match env:
        case "prod":
            autoreload = False
            loglevel = "warning"
        case "dev" | "stage":
            autoreload = True
            loglevel = "info"
            logging.basicConfig(level=logging.INFO)
        case _:
            raise ValueError(
                f"Unknown environment {env} provided. env should be one of prod, stage or dev"
            )
    uvicorn.run(
        "routers:app", host="0.0.0.0", port=8000, reload=autoreload, log_level=loglevel
    )


if __name__ == "__main__":
    load_dotenv()
    parser = cli_parser()

    # run appropriate command
    args = parser.parse_args()
    match args.command:
        case "eval":
            logging.basicConfig(level=logging.INFO)
            evaluate_cv(args.net, args.train)
        case _:
            run()
