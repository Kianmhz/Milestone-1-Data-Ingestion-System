from google.cloud import pubsub_v1
import glob
import json
import os
import csv
import sys

# Try to find a service account JSON in the current directory and set credentials
files = glob.glob("*.json")
if files:
    os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", files[0])

project_id = "cloud-pub-sub-485802"
topic_name = "csvReader"
csv_path = "Labels.csv"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)
print(f"Publishing messages to {topic_path}")

def read_csv_records(path):
    try:
        with open(path, newline='') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                # csv.DictReader returns strings (including empty strings). Keep as-is
                yield row
    except FileNotFoundError:
        print(f"CSV file not found: {path}")
        sys.exit(1)

for record in read_csv_records(csv_path):
    # Convert the record (dict of strings) into JSON and publish
    message_json = json.dumps(record)
    data = message_json.encode("utf-8")
    print(f"Producing record: {message_json}")
    future = publisher.publish(topic_path, data)
    # Block until the publish completes (optional but helpful for small scripts)
    future.result()
