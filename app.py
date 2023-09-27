from flask import Flask, request
import requests
import os

SERVICENOW_INSTANCE_URL = os.getenv("SERVICENOW_INSTANCE_URL")
SERVICE_NOW_USERNAME = os.getenv("SERVICE_NOW_USERNAME")
SERVICE_NOW_PASSWORD = os.getenv("SERVICE_NOW_PASSWORD")


app = Flask(__name__)


@app.route('/alerts', methods=['POST'])
def alerts():
    alerts = request.json['alerts']
    for alert in alerts:
        create_service_now_incident(alert)
    return "OK", 200

def create_service_now_incident(alert):
    servicenow_url = "https://"+str(SERVICENOW_INSTANCE_URL)+"/api/now/table/incident"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "short_description": alert['labels']['alertname'],
        "description": alert['annotations']['description']
    }
    response = requests.post(servicenow_url, headers=headers, auth=(SERVICE_NOW_USERNAME, SERVICE_NOW_PASSWORD), json=data)
    print(f"Incident created in ServiceNow with status code: {response.status_code}")

if __name__ == '__main__':
    app.run(port=5000)
