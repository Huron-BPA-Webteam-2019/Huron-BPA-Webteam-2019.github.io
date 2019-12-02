#!/usr/bin/env python
import os, csv, requests
from os.path import dirname, join, abspath
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import subprocess

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    join(dirname(abspath(__file__)), 'creds.json'), scope)

gc = gspread.authorize(credentials)
worksheet = gc.open_by_url(
    'https://docs.google.com/spreadsheets/d/1Gvx-VLYMUNGL-XF_SbaBiHNCO9jpsGmCFwh56LEv39s/edit#gid=0').sheet1
website = dirname(dirname(abspath(__file__)))
items = worksheet.get_all_records()
for row in items:
    if not row["filename"] or not row["url"]:
        continue

    ending = row["url"].split('.')[-1].lower()
    file_path = join(website, "assets", row["filename"] + f'.{ending or "jpg"}')
    file_path_caption = join(website, "assets", row["filename"] + f'_caption.{ending or "jpg"}')
    try:
        os.remove(file_path)
        os.remove(file_path_caption)
    except Exception:
        pass
    citation = row['citation']
    try:
        with open(file_path, 'wb') as write:
            write.write(requests.get(row["url"]).content)
            print(f'downloaded {row["filename"]}.{ending or "jpg"}')
            if citation is not None:
                print('adding citation', citation)
                # citation = citation.replace('"',"\\\"",-1)
                part1 = f'magick identify -format %w,%h "{file_path}"'
                part2 = 'magick convert -background "#00000080" -fill white -gravity center \
    -font Times-New-Roman -size {}x -pointsize {}  caption:"{}" \
    "{}" +swap -gravity North -composite "{}"'
                out = subprocess.check_output(part1, shell=True)
                num1, num2 = out.decode().split(',')
                height = int(int(num2) / 30)
                os.system(part2.format(int(num1), height, citation.replace('"','\\"'), file_path, file_path_caption))
    except Exception:
        pass