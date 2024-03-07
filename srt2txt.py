#!/usr/bin/env python
import sys
import re

def convert_srt_to_txt(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"File {input_file} doesn't exist.")
        sys.exit(1)

    with open(output_file, 'w', encoding='utf-8') as f:
        for line in lines:
            # remove bom of utf8 with bom
            line = line.lstrip('\ufeff')
            # remove dos \r
            line = line.replace('\r', '')
            # remove line numbers
            if re.match(r'^\d+$', line.strip()):
                continue
            # remove timing
            if re.match(r'^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$', line.strip()):
                continue
            # remove blank lines
            if line.strip() == '':
                continue
            # remove tags
            line = re.sub(r'<[^>]*>', '', line)
            f.write(line)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} SRTFILE OUTPUTFILE")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    convert_srt_to_txt(input_file, output_file)
    print("Conversion completed.")




# get yours from here https://www.chatpdf.com/docs/api/backend
ChatPDF_API_KEY= YOUR_KEY_HERE


import requests

sourceId = ""
headers = {
    'x-api-key': ChatPDF_API_KEY
}

files = [
    ('file', ('file', open(output_file, 'rb'), 'application/octet-stream'))
]


## add file 
response = requests.post(
    'https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files)
if response.status_code == 200:
    sourceId =response.json()['sourceId']
    print('Source ID:', sourceId)
else:
    print('Status:', response.status_code)
    print('Error:', response.text)



headers = {
    'x-api-key': ChatPDF_API_KEY,
    "Content-Type": "application/json",
}

# summarize the file
data = {
    'sourceId': sourceId,
    'messages': [
        {
            'role': "user",
            'content': "Provide me with a overview of what this document is about. The overview should be a little detailed.",
        }
    ]
}

response = requests.post(
    'https://api.chatpdf.com/v1/chats/message', headers=headers, json=data)

if response.status_code == 200:
    print('Result:', response.json()['content'])
else:
    print('Status:', response.status_code)
    print('Error:', response.text)