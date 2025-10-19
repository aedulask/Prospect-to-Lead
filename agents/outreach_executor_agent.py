import time
import random
import os
class OutreachExecutorAgent:
    """
    Demo-ready OutreachExecutorAgent:
    Simulates sending personalized outreach emails via Apollo API.
    Prints delivery status to console instead of sending real emails.
    """


    def __init__(self, apollo_api_key=None, sendgrid_api_key=None):
        self.apollo_api_key = apollo_api_key or os.getenv("APOLLO_API_KEY")
        self.sendgrid_api_key = sendgrid_api_key or os.getenv("SENDGRID_API_KEY")
        self.apollo_endpoint = "https://api.apollo.io/v1/campaigns/send_email"


    def send_email_apollo(self, lead_email, subject, body):
        """
        Simulate sending a single email via Apollo API.
        """
        # Simulate success/failure randomly for demo effect
        success = random.choice([True, True, True, False])  # 75% chance success
        if success:
            campaign_id = f"demo_{random.randint(1000,9999)}"
            print(f"[OutreachExecutorAgent] Sent email to {lead_email} (campaign_id: {campaign_id})")
            return {"lead": lead_email, "status": "sent", "campaign_id": campaign_id}
        else:
            print(f"[OutreachExecutorAgent] Failed to send email to {lead_email}")
            return {"lead": lead_email, "status": "failed", "error": "Simulated failure"}

    def run(self, messages, subject="Quick Introduction"):
        """
        Simulate sending all emails and return sent status for each.
        """
        sent_status = []
        for msg in messages:
            lead_email = msg.get("lead")
            body = msg.get("email_body")
            status = self.send_email_apollo(lead_email, subject, body)
            sent_status.append(status)
            time.sleep(0.3)  # Small delay for demo effect
        print(f"[OutreachExecutorAgent] Completed sending {len(messages)} emails.")
        return sent_status


# Demo run
if __name__ == "__main__":
    sample_messages = [
        {"lead": "john.doe@acme.com", "email_body": "Hi John, I wanted to introduce our product..."},
        {"lead": "jane.smith@beta.com", "email_body": "Hi Jane, I wanted to introduce our product..."}
    ]

    agent = OutreachExecutorAgent()
    results = agent.run(sample_messages)
    print("\n[OutreachExecutorAgent] Final Sent Status:")
    for res in results:
        print(res)
