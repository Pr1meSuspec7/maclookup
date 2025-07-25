#!/usr/bin/python3

import requests
import sys
import json
import argparse
import re
import os
from pathlib import Path


# Argument definitions
parser = argparse.ArgumentParser(description='Mac address vendor lookup.')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-m', '--mac', nargs='*', type=str, help='Mac addresses to search. \
                   Accepted forms are: colon, dot, dash. You can search for multiple mac separated by space. \
                   Example: python maclookup.py 11:22:33:44:55:66 aa-bb-cc-dd-ee-11')
group.add_argument('-u', '--update', action='store_const', const=1, help='Download the last database version from https://maclookup.app/downloads/json-database/get-db?.')
args = parser.parse_args()
# args = parser.parse_args(['-m', '00:16:9C:11:11:11 00:50:56:11:11:11'])


# Database file path
home = Path.home()
db_file = f'{home.as_posix()}/Documents/mac-vendors-export.json'


def check_db_exist(db_file):
    if os.path.isfile(db_file) is False:
        download_db(db_file)
    else:
        pass


def load_db(db_file):
    with open(db_file, 'r', encoding="utf8") as file:
        return json.load(file)


def download_db(db_file):
    print('Downloading the latest MAC address database...')
    url = 'https://maclookup.app/downloads/json-database/get-db?'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        with open(db_file, 'w', encoding="utf-8") as file:
            file.write(response.text)
        print("Database downloaded successfully.")
    else:
        print(f"Failed to download database. Status code: {response.status_code}")
        sys.exit(1)


def check_mac_syntax(mac):
    x = re.search("([0-9A-Fa-f]{2}[:.-]){5}[0-9A-Fa-f]{2}", mac)
    if x is None:
        return False
    else:
        return True


def maclookup(db, maclist):
    for mac in maclist:
        mac = mac.replace('-', ':').replace('.', ':').upper()
        if check_mac_syntax(mac) is False:
            print(f'Invalid MAC address format: {mac}')
            continue
        try:
            matches = [i for i in db if mac.startswith(i['macPrefix'])]
            if matches:
                # Select the match with the longest macPrefix
                best_match = max(matches, key=lambda x: len(x['macPrefix']))
                vendor = best_match['vendorName']
                print(f'{mac} - {vendor}')
            else:
                print(f'{mac} - Vendor not found')
        except KeyError:
            print(f'{mac} - Vendor not found')


def main():
    if args.update:
        download_db(db_file)
    else:
        maclist = args.mac
        check_db_exist(db_file)
        db = load_db(db_file)
        maclookup(db, maclist)


if __name__ == '__main__':
    main()
