#!/usr/bin/env python3
import json
import sys
import requests
import os
import subprocess

WEBHOOK_URL = os.getenv("TEAMS_WEBHOOK_URL")
if not WEBHOOK_URL:
    print("Error: TEAMS_WEBHOOK_URL not set")
    sys.exit(1)

repo = os.getenv("GITHUB_REPOSITORY", "unknown/repo")
branch = os.getenv("GITHUB_REF_NAME", "unknown-branch")
run_id = os.getenv("GITHUB_RUN_ID", "")
server_url = os.getenv("GITHUB_SERVER_URL", "https://github.com")
status = os.getenv("JOB_STATUS", "failed")  # We'll pass this manually

run_url = f"{server_url}/{repo}/actions/runs/{run_id}"

color = "Attention" if status.lower() == "failed" else "Good"


def get_committer_name():
    try:
        name = (
            subprocess.check_output(
                ["git", "log", "-1", "--pretty=format:%an"],
                stderr=subprocess.DEVNULL,
                text=True,
            )
            .strip()
        )
        return name
    except Exception:
        return "Unknown committer"


def get_commit_message():
    try:
        message = (
            subprocess.check_output(
                ["git", "log", "-1", "--pretty=format:%s"],
                stderr=subprocess.DEVNULL,
                text=True,
            )
            .strip()
        )
        return message
    except Exception:
        return "Unknown commit message"


committer = get_committer_name()
commit_message = get_commit_message()
bypass_notice = None
if commit_message.lower().startswith("bypass-check:"):
    bypass_notice = {
        "type": "TextBlock",
        "text": "⚠️ Bypassed local checks",
        "weight": "Bolder",
        "color": "Warning",
        "wrap": True
    }

body = [
    {
        "type": "TextBlock",
        "text": f"CI {'Failure' if status.lower() == 'failed' else 'Success'} on {branch}",
        "weight": "Bolder",
        "size": "Medium",
        "color": color
    },
    {
        "type": "TextBlock",
        "text": f"Repository: {repo}\nBranch: {branch}",
        "wrap": True
    },
    {
        "type": "TextBlock",
        "text": f"[View Workflow Run]({run_url})",
        "wrap": True
    },
    {
        "type": "TextBlock",
        "text": f"Committer: {committer}",
        "wrap": True
    },
]
if bypass_notice:
    body.append(bypass_notice)

payload = {
    "attachments": [
        {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "type": "AdaptiveCard",
                "version": "1.4",
                "body": body,
            }
        }
    ]
}

try:
    response = requests.post(
        WEBHOOK_URL,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload)
    )
    print(f"Response status: {response.status_code}")
    print(response.text)
except Exception as e:
    print(f"Error sending notification: {e}")
    sys.exit(1)
