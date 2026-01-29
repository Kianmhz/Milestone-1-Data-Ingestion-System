Project: CSV → Google Pub/Sub producer & consumer

This small project demonstrates publishing CSV rows as JSON messages to Google Cloud Pub/Sub and a subscriber that deserializes and prints them.

Files
- `producer.py` — Reads `Labels.csv`, converts each CSV row to a Python dict, serializes to JSON, and publishes to a Pub/Sub topic.
- `consumer.py` — Subscribes to a Pub/Sub subscription, receives messages, deserializes JSON to dict, and prints the key/value pairs.
- `Labels.csv` — Example CSV file used by `producer.py`.

Quick checklist (requirements mapping)
- Producer script: read CSV, convert rows → dict, serialize, publish. (10 pts)
- Consumer script: receive messages, deserialize to dict, print values. (5 pts)
- GCP tools / credentials: instructions to set up topic/subscription and credentials. (5 pts)

Prerequisites
- Python 3.8+ and pip
- A Google Cloud project with Pub/Sub API enabled
- A service account JSON key with Pub/Sub Publisher/Subscriber permissions

Install dependencies
```bash
python3 -m pip install --user google-cloud-pubsub
```

Credentials
- Place your service account JSON key in the project folder (the scripts auto-detect the first `*.json` file and set `GOOGLE_APPLICATION_CREDENTIALS`).

Default configuration used by the scripts
- `project_id` in both scripts = `cloud-pub-sub-485802`
- `topic_name` in `producer.py` = `csvReader`
- `subscription_id` in `consumer.py` = `testTopic-sub`

Run the consumer (start first)
```bash
python3 consumer.py
```

Run the producer (publishes every CSV row)
```bash
python3 producer.py
```

What you'll observe
- `producer.py` prints lines like:
  Producing record: {"time":"...","profileName":"denver",...}
- `consumer.py` prints each consumed record as:
  Consumed record:
    time: ...
    profileName: ...
    temperature: ...
    humidity: ...
    pressure: ...
