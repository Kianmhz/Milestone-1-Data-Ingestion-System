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
- (Optional) `gcloud` CLI for convenience

Install dependencies
```bash
python3 -m pip install --user google-cloud-pubsub
```

Credentials
- Place your service account JSON key in the project folder (the scripts auto-detect the first `*.json` file and set `GOOGLE_APPLICATION_CREDENTIALS`).
- Or set it explicitly in your shell:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/path/to/key.json"
```

Default configuration used by the scripts
- `project_id` in both scripts = `cloud-pub-sub-485802`
- `topic_name` in `producer.py` = `csvReader`
- `subscription_id` in `consumer.py` = `testTopic-sub`

Ensure the following Pub/Sub resources exist (adjust names in scripts or here to match):
```bash
gcloud config set project YOUR_PROJECT_ID
# create topic
gcloud pubsub topics create csvReader
# create subscription bound to the topic
gcloud pubsub subscriptions create testTopic-sub --topic=csvReader
```

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

Quick manual tests (optional)
- Publish a manual message:
```bash
gcloud pubsub topics publish csvReader --message='{"test":"ok"}'
```
- Pull messages from subscription:
```bash
gcloud pubsub subscriptions pull testTopic-sub --limit=1 --auto-ack
```

Notes, edge cases and recommendations
- CSV empty fields remain empty strings; you can post-process (e.g., convert to None or float) before serializing if desired.
- Current `producer.py` uses `future.result()` to block until each message is published. For large CSVs consider using batching or not awaiting each publish for higher throughput.
- `consumer.py` acks messages even on JSON decoding errors to avoid redelivery in this simple example; change to `message.nack()` if you want retries.
- Add CLI flags to override `project_id`, `topic_name`, `subscription_id`, and `csv_path` for flexibility.

Grading summary (suggested phrasing for your report)
- Producer (10 pts): Implements CSV read → dict → JSON → publish to Pub/Sub. (Status: Done)
- Consumer (5 pts): Implements Pub/Sub subscriber → JSON → dict → print. (Status: Done)
- GCP tools (5 pts): Instructions and commands to set credentials and create topic/subscription are provided. (Status: Done)

Contact / next steps
- To make the project more robust I can: add CLI args, add logging, or change publish to batched/asynchronous mode. Tell me which and I will update the repo.
