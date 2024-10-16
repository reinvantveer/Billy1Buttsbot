import argparse
import sys
import tomllib
from argparse import Namespace

from loguru import logger

from buttify.billy1buttsbot import Billy1ButtsBot
from buttify.settings import Settings


def main(args: Namespace) -> None:
    with open(args.config, "rb") as f:
        config = tomllib.load(f)["tool"]["billy1buttsbot"]

    # Set the verbosity of the logger.
    if config['verbose']:
        logger.remove()
        logger.add(sys.stderr, level="DEBUG")
    else:
        logger.remove()
        logger.add(sys.stderr, level="INFO")

    token = input("Enter the Twitch OAuth token: ")
    logger.debug("Verbose logging enabled.")

    settings = Settings(
        channel=str(config['channel']),
        user=config['username'],
        token=token,
        ignore_users=list(config['ignore_users']),
        chance=float(config["chance_of_buttification"]),
        dry_run=config["dry_run"],
    )

    if settings.dry_run:
        logger.warning("Running in dry-run mode. No messages will be sent.")

    bot = Billy1ButtsBot(settings)
    logger.info("Starting Billy1ButtsBot... press Ctrl+C to stop.")
    bot.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Billy1ButtsBot service')
    parser.add_argument('--config', default='pyproject.toml', help='Configuration')

    args = parser.parse_args()
    main(args)
