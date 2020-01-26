#!/usr/bin/env python3
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
i = 1
total = len(items)
for row in items:
    if row["filename"] is "" or row["url"] is "":
        continue

    ending = row["url"].split('.')[-1].lower().replace('jpeg', 'jpg', -1)
    img_src = join(row["filename"] + f'.{ending or "jpg"}')
    with open(join(website,'pages','format.html'), 'a') as file:
        file.write(f'<img src="/assets/{img_src}" alt="{row["filename"]}">\n')
    file_path = join(website, "assets", row["filename"] + f'.{ending or "jpg"}')
    file_path_caption = join(website, "assets", row["filename"] + f'_caption.{ending or "jpg"}')
    try:
        os.remove(file_path)
        os.remove(file_path_caption)
    except Exception as e:
        # print(f'Could not delete {row["filename"]} and/or it\'s captioned version.')
        pass

    citation = row['citation']
    with open(file_path, 'wb') as write:
        write.write(requests.get(row["url"]).content)
        
    print(f'[{i}/{total}] {row["filename"]}.{ending or "jpg"} Downloaded')
    i += 1
    if citation is not "":
        part1 = f'magick identify -format %w,%h "{file_path}"'
        font = 'Times-Roman'
        if os.name == 'nt':
            font = 'Times-New-Roman'
        
        part2 = 'magick convert -background "#00000080" -fill white -gravity center \
        -font {} -size {}x -pointsize {}  caption:"{}" \
        "{}" +swap -gravity North -composite "{}"'
        try:
            out = subprocess.check_output(part1, shell=True)
        except subprocess.CalledProcessError:
            print(f'Error checking dimensions of image. Not a JPEG File: starts with may mean the picture is a PNG.\n{row["url"]}')
            continue
        num1, num2 = out.decode().split(',')
        height = int(int(num2) / 30)
        citation = citation.replace('"', '\\"')
        caption_command = part2.format(font, int(num1), height, citation, file_path, file_path_caption)
        try:
            os.system(caption_command)
            print(f'{row["filename"]}.{ending or "jpg"} Cited ({citation[:10]}...{citation[-10:]})')
        except Exception as e:
            print('Caption Error:', e)

