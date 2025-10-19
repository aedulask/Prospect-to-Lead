import os
import requests
import time

class ResponseTrackerAgent:
    """
    ResponseTrackerAgent:
    Monitors email responses, opens, clicks, and meeting bookings
    for sent campaigns using Apollo API.
    """

    def __init__(self, apollo_api_key=None):
        self.apollo_api_key = apollo_api_key or os.getenv("APOLLO_API_KEY")
        self.tracking_endpoint = "https://api.apollo.io/v1/campaigns/responses"

    def get_campaign_responses(self, campaign_id):
        """
        Fetch responses for a single campaign ID.
        """
        headers = {"Authorization": f"Bearer {self.apollo_api_key}"}
        params = {"campaign_id": campaign_id}

        try:
            response = requests.get(self.tracking_endpoint, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            # Map to workflow schema
            responses = []
            for r in data.get("results", []):
                responses.append({
                    "lead": r.get("email"),
                    "opened": r.get("opened", False),
                    "clicked": r.get("clicked", False),
                    "replied": r.get("replied", False),
                    "meeting_booked": r.get("meeting_booked", False),
                    "timestamp": r.get("timestamp")
                })
            return responses
        except Exception as e:
            print(f"[Apollo API Error]: {e} for campaign {campaign_id}")
            return []

    def run(self, campaign_ids):
        """
        Track responses for a list of campaign_ids.
        """
        all_responses = []
        for cid in campaign_ids:
            responses = self.get_campaign_responses(cid)
            all_responses.extend(responses)
            time.sleep(0.5)  # Respect API rate limits
        return all_responses


# Example usage
if __name__ == "__main__":
    sample_campaign_ids = ["campaign_12345", "campaign_67890"]

    agent = ResponseTrackerAgent()
    responses = agent.run(sample_campaign_ids)
    for r in responses:
        print(r)
