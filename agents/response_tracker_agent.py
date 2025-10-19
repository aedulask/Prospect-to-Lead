import time
import random
import os
class ResponseTrackerAgent:
    """
    Demo-ready ResponseTrackerAgent:
    Simulates tracking email responses, clicks, replies, and meetings.
    """

    def __init__(self, apollo_api_key=None):
        self.apollo_api_key = apollo_api_key or os.getenv("APOLLO_API_KEY")
        self.tracking_endpoint = "https://api.apollo.io/v1/campaigns/responses"

    def get_campaign_responses(self, campaign_id):
        """
        Generate fake responses for a single campaign.
        """
        fake_leads = [
            "john.doe@acme.com",
            "jane.smith@beta.com",
            "alice@gamma.com",
            "bob@delta.com"
        ]
        responses = []
        for lead in fake_leads:
            response = {
                "lead": lead,
                "opened": random.choice([True, True, False]),
                "clicked": random.choice([True, False, False]),
                "replied": random.choice([True, False, False, False]),
                "meeting_booked": random.choice([True, False, False, False]),
                "timestamp": time.time(),
                "campaign_id": campaign_id
            }
            responses.append(response)
            print(f"[ResponseTrackerAgent] Tracked response: {response}")
        return responses

    def run(self, campaign_ids):
        """
        Track responses for a list of campaign_ids (demo mode).
        """
        all_responses = []
        for cid in campaign_ids:
            responses = self.get_campaign_responses(cid)
            all_responses.extend(responses)
            time.sleep(0.3)  # Small delay for demo effect
        print(f"[ResponseTrackerAgent] Total responses tracked: {len(all_responses)}")
        return all_responses


# Demo run
if __name__ == "__main__":
    sample_campaign_ids = ["demo_1234", "demo_5678"]

    agent = ResponseTrackerAgent()
    responses = agent.run(sample_campaign_ids)
    print("\n[ResponseTrackerAgent] Final Responses:")
    for r in responses:
        print(r)
