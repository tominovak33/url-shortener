# Make sure App Engine APK is available
import sys
import csv
# This is intented to run from the command line, so add in the right SDK manually
sys.path.append('/home/tomi/google_appengine')

from google.appengine.api.files import records
from google.appengine.datastore import entity_pb
from google.appengine.api import datastore

raw = open('datastore_backup_datastore_backup_2017_01_08_Url', 'r')

reader = records.RecordsReader(raw)

with open('export.csv', 'wb') as f:
    w = csv.DictWriter(f, ['date_created', 'full_url', 'short_url'])
    w.writeheader()

    for record in reader:
        entity_proto = entity_pb.EntityProto(contents=record)
        entity = datastore.Entity.FromPb(entity_proto)
        w.writerow(entity)
