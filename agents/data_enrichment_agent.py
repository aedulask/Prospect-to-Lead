import time

class DataEnrichmentAgent:
    """
    Demo-ready DataEnrichmentAgent:
    Returns fake enriched lead data instead of calling PDL or Clearbit.
    Fully console-friendly for demo purposes.
    """

    def __init__(self):
        pass  # No API key needed for demo

    def enrich_lead(self, lead):
        """
        Generate fake enrichment data for a single lead.
        """
        enriched = {
            "company": lead.get("company"),
            "contact": lead.get("contact_name"),
            "role": "CTO",  # Demo role
            "technologies": ["Python", "AWS"],  # Demo tech stack
            "employee_count": 150,  # Demo employee count
            "revenue": 50000000  # Demo revenue
        }
        print(f"[DataEnrichmentAgent] Enriched lead: {enriched}")
        return enriched

    def run(self, leads):
        """
        Enrich a list of leads (demo mode).
        """
        enriched_leads = []
        for lead in leads:
            enriched = self.enrich_lead(lead)
            enriched_leads.append(enriched)
            time.sleep(0.2)  # Small delay for demo effect
        print(f"[DataEnrichmentAgent] Completed enriching {len(leads)} leads.")
        return enriched_leads


# Demo run
if __name__ == "__main__":
    sample_leads = [
        {"company": "Acme Corp", "contact_name": "John Doe", "email": "john.doe@acme.com"},
        {"company": "Beta Inc", "contact_name": "Jane Smith", "email": "jane.smith@beta.com"}
    ]

    agent = DataEnrichmentAgent()
    enriched = agent.run(sample_leads)
    print("\n[DataEnrichmentAgent] Final Enriched Leads:")
    for lead in enriched:
        print(lead)
