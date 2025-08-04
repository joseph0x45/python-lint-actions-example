# import requests
# import json
import pymsteams

ms_teams_webhook = "https://defaultc54cdfa638d740828115599a0c8647.d9.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/15122db31f144ab292565c0f400a31c7/triggers/manual/paths/invoke/?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=QZbnfQ6wQz4cDwivg41KNmlaTbSaaEvq6aV2IBWnCfg"

# webhook_url = ms_teams_webhook
# message_text = "Hello from Python! This is an automated message."
#
# headers = {"Content-Type": "application/json"}
# payload = {"text": message_text}
#
# response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
#
# if response.status_code == 200:
#     print("Message sent successfully!")
# else:
#     print(f"Failed to send message. Status code: {response.status_code}")
#     print(response.text)


webhook_url = ms_teams_webhook
message_text = "Hello from pymsteams! This is an automated message."

myTeamsMessage = pymsteams.connectorcard(webhook_url)
myTeamsMessage.text(message_text)
myTeamsMessage.send()

print("Message sent successfully!")
