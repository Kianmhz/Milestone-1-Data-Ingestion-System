from google.cloud import pubsub_v1
import glob
import json
import os
import sys

# Try to find a service account JSON in the current directory and set credentials
files = glob.glob("*.json")
if files:
    os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", files[0])

project_id = "cloud-pub-sub-485802"
subscription_id = "csvReader-sub"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

print(f"Listening for messages on {subscription_path}..\n")

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    try:
        payload = message.data.decode("utf-8")
        record = json.loads(payload)
    except Exception as e:
        print(f"Failed to decode message: {e}")
        # Acknowledge to avoid redelivery in this simple example
        message.ack()
        return

    print("Consumed record:")
    for k, v in record.items():
        print(f"  {k}: {v}")

    message.ack()

with subscriber:
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()

