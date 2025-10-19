import os
import requests
import time

class DataEnrichmentAgent:
    """
    DataEnrichmentAgent:
    Enriches lead data with additional information like roles, technologies, company info.
    Uses People Data Labs (PDL) API as an alternative to Clearbit.
    """

    def __init__(self, pdl_api_key=None):
        self.pdl_api_key = pdl_api_key or os.getenv("PDL_API_KEY")
        self.pdl_endpoint = "https://api.peopledatalabs.com/v5/person/enrich"

    def enrich_lead(self, lead):
        """
        Enrich a single lead using PDL API.
        """
        payload = {
            "email": lead.get("email"),
            "company": lead.get("company"),
            "api_key": self.pdl_api_key
        }
        try:
            response = requests.get(self.pdl_endpoint, params=payload)
            response.raise_for_status()
            data = response.json()

            enriched = {
                "company": lead.get("company"),
                "contact": lead.get("contact_name"),
                "role": data.get("job_title") or "N/A",
                "technologies": data.get("tech", []),
            }
            return enriched
        except Exception as e:
            print(f"[PDL API Error]: {e} for lead {lead.get('email')}")
            return {
                "company": lead.get("company"),
                "contact": lead.get("contact_name"),
                "role": "N/A",
                "technologies": []
            }

    def run(self, leads):
        """
        Main method to enrich a list of leads.
        """
        enriched_leads = []
        for lead in leads:
            enriched = self.enrich_lead(lead)
            enriched_leads.append(enriched)
            time.sleep(0.5)  # Respect API rate limits
        return enriched_leads


# Example usage
if __name__ == "__main__":
    sample_leads = [
        {"company": "Acme Corp", "contact_name": "John Doe", "email": "john.doe@acme.com"}
    ]

    agent = DataEnrichmentAgent()
    enriched = agent.run(sample_leads)
    for lead in enriched:
        print(lead)
