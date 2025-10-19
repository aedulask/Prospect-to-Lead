import time
import random
import os
class ProspectSearchAgent:
    """
    Demo-ready ProspectSearchAgent:
    Simulates searching for B2B prospects using ICP and signals.
    Returns fake leads from Clay and Apollo for demo purposes.
    """

    def __init__(self, clay_api_key=None, apollo_api_key=None):
        self.clay_api_key = clay_api_key or os.getenv("CLAY_API_KEY")
        self.apollo_api_key = apollo_api_key or os.getenv("APOLLO_API_KEY")
        self.clay_endpoint = "https://api.clay.com/search"
        self.apollo_endpoint = "https://api.apollo.io/v1/mixed_search"

    def generate_fake_lead(self, source):
        """
        Generate a single fake lead.
        """
        companies = ["Acme Corp", "Beta Inc", "Gamma LLC", "Delta Solutions"]
        contacts = ["John Doe", "Jane Smith", "Alice Johnson", "Bob Lee"]
        emails = ["john@acme.com", "jane@beta.com", "alice@gamma.com", "bob@delta.com"]
        signals = ["recent_funding", "hiring_for_sales"]
        idx = random.randint(0, 3)
        lead = {
            "company": companies[idx],
            "contact_name": contacts[idx],
            "email": emails[idx],
            "linkedin": f"https://linkedin.com/in/{contacts[idx].replace(' ', '').lower()}",
            "signal": random.choice(signals),
            "source": source
        }
        print(f"[ProspectSearchAgent] {source} lead generated: {lead}")
        return lead

    def search_clay(self, icp, signals):
        """
        Simulate Clay API search.
        """
        time.sleep(0.3)
        return [self.generate_fake_lead("Clay") for _ in range(2)]

    def search_apollo(self, icp, signals):
        """
        Simulate Apollo API search.
        """
        time.sleep(0.3)
        return [self.generate_fake_lead("Apollo") for _ in range(2)]

    def run(self, icp, signals):
        """
        Generate combined fake leads for demo.
        """
        clay_leads = self.search_clay(icp, signals)
        apollo_leads = self.search_apollo(icp, signals)
        combined = clay_leads + apollo_leads
        # Deduplicate by email
        unique_leads = {lead['email']: lead for lead in combined}.values()
        print(f"[ProspectSearchAgent] Total unique leads: {len(unique_leads)}")
        return list(unique_leads)


# Demo run
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
    print("\n[ProspectSearchAgent] Final Leads:")
    for lead in leads:
        print(lead)
