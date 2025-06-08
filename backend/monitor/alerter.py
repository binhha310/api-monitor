import requests

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/xxxx/yyyy/zzzz"

def send_slack_alert(message: str):
    payload = {
        "text": message
    }
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    if response.status_code != 200:
        print(f"Failed to send Slack alert: {response.text}")
