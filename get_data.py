'''
Sajid Farook

This script uses DocumentCloud API to:
1) Download text of BLN AgendaWatch, one txt file per pdf
2) Download a CSV of metadata on each such document

The first column of the CSV coresponds to the name of the txt file.
'''

from documentcloud import DocumentCloud
import argparse 
import csv
import pandas as pd
import os
import requests

# DocumentCloud credentials
USERNAME = '<your DCloud username>'
PASSWORD = '<your DCloud password>' # input your credentials

BLN_ID = "11341"
client = DocumentCloud(USERNAME, PASSWORD)
BLNDocs = client.documents.list(organization=BLN_ID)  # access BLN DocumentCloud

'''
Downloads txt files of documents into 'txt_files' folder (creates if it doesn't exist).
Specify how many documents you want to download, or all if non specified (which is around 8000 as of April 2024).
Downloading all 8000ish can take a while though
'''
def download_txt_corpus(numdocs=None):

    os.makedirs('txt_files', exist_ok=True)  # Creates the folder if it doesn't exist

    if numdocs == None:
        for document in BLNDocs:  # download entire corpus
            file_name = f"txt_files/{document.id}.txt"   # store document as "<idnumber>.txt"
            with open(file_name, "w") as file:
                file.write(document.full_text)
    else:
        for i, document in enumerate(BLNDocs): 
            file_name = f"txt_files/{document.id}.txt"
            with open(file_name, "w") as file:
                file.write(document.full_text)
            if i == numdocs:  # only download first numdocs documents
                break

'''
Constructs a CSV file containing metadata of documents. Metadata includes ID number from DocumentCloud, url for viewing 
via. DocumentCloud, as well as all custom metadata that Big Local News has provided

Again specify number of documents to include in CSV or don't to populate CSV with all documents (8000ish), though this is 
much quicker than downloading all 8000 txt files.
'''
def create_csv_from_metadata(numdocs=None):
    csv_file_path = 'metadata.csv'
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write the header row
        BLN_metadata = ['place', 'state', 'file_ext', 'place_id', 'platform', 'asset_name', 
                  'asset_type', 'source_url', 'document_id', 'content_type', 'meeting_date', 
                  'committee_name', 'committee_slug', 'content_length', 'agenda_watch_pk']
        csv_writer.writerow(['txt_title_num'] + BLN_metadata + ['canonical_url'])

        # Iterate over each document
        if numdocs is None:
            for document in BLNDocs:
                metadata = document.data 
                row_data = [document.id] + [metadata.get(key, '') for key in BLN_metadata] + [document.canonical_url]
                csv_writer.writerow(row_data)
        else:
            for i, document in enumerate(BLNDocs):
                metadata = document.data 
                row_data = [document.id] + [metadata.get(key, '') for key in BLN_metadata] + [document.canonical_url]
                csv_writer.writerow(row_data)
                if i == numdocs:
                    break

# Sample usage to download 100 txt files and construct entire CSV of metadata
number_of_txts = 100
download_txt_corpus()
print("Finished downloading ", number_of_txts, " documents. Now constructing metadata csv...")
#create_csv_from_metadata()

