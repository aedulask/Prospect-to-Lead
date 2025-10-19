import os
import requests

class ProspectSearchAgent:
    """
    ProspectSearchAgent:
    Searches for B2B prospects using ICP (industry, location, revenue, employee count)
    and signals (recent funding, hiring for sales) from Clay and Apollo APIs.
    """

    def __init__(self, clay_api_key=None, apollo_api_key=None):
        self.clay_api_key = clay_api_key or os.getenv("CLAY_API_KEY")
        self.apollo_api_key = apollo_api_key or os.getenv("APOLLO_API_KEY")
        self.clay_endpoint = "https://api.clay.com/search"
        self.apollo_endpoint = "https://api.apollo.io/v1/mixed_search"

    def search_clay(self, icp, signals):
        """
        Call Clay API to search for companies matching the ICP.
        Returns list of leads.
        """
        headers = {"Authorization": f"Bearer {self.clay_api_key}"}
        payload = {"icp": icp, "signals": signals}
        try:
            response = requests.post(self.clay_endpoint, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            # Map to your output schema
            leads = [
                {
                    "company": lead.get("company_name"),
                    "contact_name": lead.get("contact_name"),
                    "email": lead.get("email"),
                    "linkedin": lead.get("linkedin"),
                    "signal": lead.get("signal"),
                }
                for lead in data.get("results", [])
            ]
            return leads
        except Exception as e:
            print(f"[Clay API Error]: {e}")
            return []

    def search_apollo(self, icp, signals):
        """
        Call Apollo API to search for companies/contacts.
        Returns list of leads.
        """
        headers = {"Authorization": f"Bearer {self.apollo_api_key}"}
        payload = {"icp": icp, "signals": signals}
        try:
            response = requests.post(self.apollo_endpoint, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            leads = [
                {
                    "company": lead.get("company_name"),
                    "contact_name": lead.get("contact_name"),
                    "email": lead.get("email"),
                    "linkedin": lead.get("linkedin"),
                    "signal": lead.get("signal"),
                }
                for lead in data.get("results", [])
            ]
            return leads
        except Exception as e:
            print(f"[Apollo API Error]: {e}")
            return []

    def run(self, icp, signals):
        """
        Main method to run prospect search.
        Returns combined leads from Clay and Apollo.
        """
        clay_leads = self.search_clay(icp, signals)
        apollo_leads = self.search_apollo(icp, signals)
        combined = clay_leads + apollo_leads
        # Optional: deduplicate leads based on email or company
        unique_leads = {lead['email']: lead for lead in combined}.values()
        return list(unique_leads)


# Example usage
if __name__ == "__main__":
    icp = {
        "industry": "SaaS",
        "location": "USA",
        "employee_count": {"min": 100, "max": 1000},
        "revenue": {"min": 20000000, "max": 200000000}
    }
    signals = ["recent_funding", "hiring_for_sales"]

    agent = ProspectSearchAgent()
    leads = agent.run(icp, signals)
    print(f"Found {len(leads)} leads")
    for lead in leads:
        print(lead)
