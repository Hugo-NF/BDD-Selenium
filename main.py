import argparse
import logging
from definitions import *
from logging.handlers import RotatingFileHandler
from datetime import datetime
import os
import json
import yaml
from utils import *
from generators import *


# PEP 8 Conventions
# https://www.python.org/dev/peps/pep-0008/#overriding-principle

def setup_logging():
    try:
        with open('settings.json', 'r') as settings_file:
            env_settings = json.load(settings_file)
            env_settings = env_settings['logging']

            path_format = get_value_or_default(env_settings, 'path_format', "logs/SeleniumBDD_{datetime}.log")
            minimum_level = get_value_or_default(env_settings, 'minimum_level', "INFO")
            file_count_limit = get_value_or_default(env_settings, 'file_count_limit', 7)
            file_size_limit_bytes = get_value_or_default(env_settings, 'file_size_limit_bytes', 128000000)
            writing_mode = get_value_or_default(env_settings, 'writing_mode', "a")
            log_format = get_value_or_default(env_settings, 'log_format', "%(asctime)s :: %(levelname)s - %(message)s")
            asctime_format = get_value_or_default(env_settings, 'asctime_format', "%d/%m/%y %H:%M:%S")
            encoding = get_value_or_default(env_settings, 'encoding', 'utf8')
            flush_delay = get_value_or_default(env_settings, 'flush_delay', False)

            # Setting configuration for logger instance 'SeleniumBDD.root'
            logger = logging.getLogger(LOGGER_INSTANCE)
            logger.setLevel(minimum_level)

            # Setting configuration for console
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)

            # File Handler config
            file_handler = RotatingFileHandler(path_format.format(datetime=datetime.now().date()),
                                               writing_mode,
                                               file_size_limit_bytes,
                                               file_count_limit,
                                               encoding,
                                               flush_delay)

            file_formatter = logging.Formatter(log_format, asctime_format)
            file_handler.setLevel(minimum_level)
            file_handler.setFormatter(file_formatter)
            console_handler.setFormatter(file_formatter)

            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

    except FileNotFoundError:
        print("FATAL ERROR: settings.json file %s do NOT exists." % args.environment)
        exit(ErrorCodes.MISSING_SETTINGS)


if __name__ == '__main__':
    # Setting up log module
    setup_logging()

    logger = logging.getLogger(LOGGER_INSTANCE)

    # Adding a new argument parser (CLI inputs)
    parser = argparse.ArgumentParser(description='BDD Tester with Selenium',
                                     epilog="")

    logger.info("Starting a new session for {user}. PID: {pid}.".format(user=os.getlogin(), pid=os.getpid()))

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-env', '--environment', nargs='?',
                       help='Path to json environment file, contains all needed variables to start the program')
    group.add_argument('-g', '--generate', nargs='+',
                       help='Generator command.'
                            '\n\tYou can use this tool to generate the files needed, probably inside a new project.'
                            '\n\tAvaliable options:'
                            '\n\t\tENV [output_path]: generates a new environment json file'
                            '\n\t\tFEATURES [output_path]: generates a new features path with examples'
                            '\n\t\tALL [output_path]: generates everything you need')

    parser.add_argument('--features', nargs='?',
                        help="Path to features folder. Not needed when using environment json.")
    parser.add_argument('--factories', nargs='?',
                        help="Path to factories folder. Not needed when using environment json.")
    parser.add_argument('--scenarios', nargs='?',
                        help="Path to scenarios folder. Not needed when using environment json.")
    parser.add_argument('-r', '--root', nargs='?',
                        help="Root address of the application. Not needed when using environment json.")
    parser.add_argument('-l', '--locale', nargs="?", default='en-US',
                        choices=['pt-BR', 'en-US'], help='Change the locale of your files. '
                                                         'Not needed when using environment json.')

    args = parser.parse_args()

    if args.generate:
        try:
            generator = generators[args.generate[0]]
            generator(args.generate[1])
        except KeyError:
            print("Error: Unknown %s generator option" % args.generate[1])

    elif args.environment:
        print("Environment option loading")

    elif args.features and args.factories and args.scenarios and args.root:
        print("Specified options")

    else:
        print("Missing options")
