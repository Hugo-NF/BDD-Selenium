import argparse
import json
import yaml
from Utils import *

# PEP 8 Conventions
# https://www.python.org/dev/peps/pep-0008/#overriding-principle

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='BDD Tester with Selenium',
                                     epilog="")

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-env', '--environment', nargs='?',
                        help='Path to json environment file')
    group.add_argument('-g', '--generate', nargs='+',
                        help='Generator command')

    parser.add_argument('--features', nargs='?',
                       help="Path to features folder")
    parser.add_argument('--factories', nargs='?',
                        help="Path to factories folder")
    parser.add_argument('--scenarios', nargs='?',
                        help="Path to scenarios folder")
    parser.add_argument('-r', '--root', nargs='?',
                        help="Root address of the application")
    parser.add_argument('-l', '--locale', nargs="?", default='en-US',
                       choices=['pt-BR', 'en-US'], help='Change locale')

    args = parser.parse_args()
    print(args.generate)
    try:
        with open(args.environment, 'r') as env_file:
            env_settings = json.load(env_file)
    except FileNotFoundError:
        print("Environment file %s do NOT exists. Do have one? Run:\n\tSeleniumBDD.py -g env {filename}.json" % args.environment)
