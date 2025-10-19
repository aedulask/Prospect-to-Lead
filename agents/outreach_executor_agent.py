import os
import requests

class OutreachExecutorAgent:
    """
    OutreachExecutorAgent:
    Sends personalized outreach emails via Apollo API or SendGrid and logs delivery status.
    """

    def __init__(self, apollo_api_key=None, sendgrid_api_key=None):
        self.apollo_api_key = apollo_api_key or os.getenv("APOLLO_API_KEY")
        self.sendgrid_api_key = sendgrid_api_key or os.getenv("SENDGRID_API_KEY")
        self.apollo_endpoint = "https://api.apollo.io/v1/campaigns/send_email"
        # If using SendGrid, you can add its endpoint here

    def send_email_apollo(self, lead_email, subject, body):
        """
        Send a single email via Apollo API.
        """
        headers = {"Authorization": f"Bearer {self.apollo_api_key}"}
        payload = {
            "to": lead_email,
            "subject": subject,
            "body": body
        }
        try:
            response = requests.post(self.apollo_endpoint, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return {"lead": lead_email, "status": "sent", "campaign_id": data.get("campaign_id")}
        except Exception as e:
            print(f"[Apollo API Error]: {e} for {lead_email}")
            return {"lead": lead_email, "status": "failed", "error": str(e)}

    def run(self, messages, subject="Quick Introduction"):
        """
        Send all emails and return sent status for each.
        """
        sent_status = []
        for msg in messages:
            lead_email = msg.get("lead")
            body = msg.get("email_body")
            status = self.send_email_apollo(lead_email, subject, body)
            sent_status.append(status)
        return sent_status


# Example usage
if __name__ == "__main__":
    sample_messages = [
        {
            "lead": "john.doe@acme.com",
            "email_body": "Hi John, I wanted to introduce our product..."
        }
    ]

    agent = OutreachExecutorAgent()
    results = agent.run(sample_messages)
    for res in results:
        print(res)
