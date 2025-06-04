import os
import requests
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText

# Config
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
REPOS = ["helix-editon/helix", "hsutter/cppfront", "LadybirdBrowser/ladybird", "jenkinsci/jenkins", "opencv/opencv"]
EMAIL_FROM = "[REDACTED]"
EMAIL_TO = "[REDACTED]"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = os.environ["SMTP_USER"]
SMTP_PASS = os.environ["SMTP_PASS"]

yesterday = (datetime.utcnow() - timedelta(days=1)).isoformat()

def fetch_changes(repo):
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    url = f"https://api.github.com/repos/{repo}/issues?since={yesterday}"
    r = requests.get(url, headers=headers)
    return r.json()

def main():
    summary = ""
    for repo in REPOS:
        changes = fetch_changes(repo)
        summary += f"\n\nChanges for {repo}:\n"
        for item in changes:
            summary += f"- {item['title']} ({item['html_url']})\n"
    msg = MIMEText(summary)
    msg["Subject"] = "Daily GitHub Report"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    with smtplib.SMTP_SSL(SMTP_SERVER) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(EMAIL_FROM, [EMAIL_TO], msg.as_string())

if __name__ == "__main__":
    main()
