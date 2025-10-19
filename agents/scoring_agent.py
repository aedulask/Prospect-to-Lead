class ScoringAgent:
    """
    Demo-ready ScoringAgent:
    Scores enriched leads based on configurable ICP criteria and returns ranked leads.
    """

    def __init__(self, scoring_criteria=None):
        """
        scoring_criteria: dict defining weights for scoring
        Example:
        {
            "employee_count": 0.3,
            "revenue": 0.3,
            "role_match": 0.2,
            "tech_stack_match": 0.2
        }
        """
        self.scoring_criteria = scoring_criteria or {
            "employee_count": 0.3,
            "revenue": 0.3,
            "role_match": 0.2,
            "tech_stack_match": 0.2
        }

    def score_lead(self, lead):
        """
        Returns a numeric score for a single lead.
        """
        score = 0

        # Employee count score (demo: prefer 100-1000)
        employee_count = lead.get("employee_count", 0)
        if 100 <= employee_count <= 1000:
            score += self.scoring_criteria["employee_count"]

        # Revenue score (demo: prefer 20M-200M)
        revenue = lead.get("revenue", 0)
        if 20_000_000 <= revenue <= 200_000_000:
            score += self.scoring_criteria["revenue"]

        # Role match (demo: prefer "CEO", "CTO", "VP Sales", "Founder")
        preferred_roles = ["CEO", "CTO", "VP Sales", "Founder"]
        role = lead.get("role", "").lower()
        if any(r.lower() in role for r in preferred_roles):
            score += self.scoring_criteria["role_match"]

        # Tech stack match (demo: has Python, Salesforce, AWS)
        desired_tech = ["Python", "Salesforce", "AWS"]
        technologies = lead.get("technologies", [])
        if any(tech in technologies for tech in desired_tech):
            score += self.scoring_criteria["tech_stack_match"]

        return score

    def run(self, enriched_leads):
        """
        Score all leads and return them sorted by descending score.
        """
        scored_leads = []
        for lead in enriched_leads:
            lead_score = self.score_lead(lead)
            lead["score"] = lead_score
            print(f"[ScoringAgent] Lead scored: {lead}")
            scored_leads.append(lead)

        # Sort by score descending
        ranked_leads = sorted(scored_leads, key=lambda x: x["score"], reverse=True)
        print(f"[ScoringAgent] Ranked {len(ranked_leads)} leads")
        return ranked_leads


# Demo run
if __name__ == "__main__":
    sample_leads = [
        {
            "company": "Acme Corp",
            "contact": "John Doe",
            "role": "CTO",
            "technologies": ["Python", "AWS"],
            "employee_count": 150,
            "revenue": 50000000
        },
        {
            "company": "Beta Inc",
            "contact": "Jane Smith",
            "role": "Manager",
            "technologies": ["JavaScript"],
            "employee_count": 50,
            "revenue": 10000000
        }
    ]

    agent = ScoringAgent()
    ranked = agent.run(sample_leads)
    print("\n[ScoringAgent] Final Ranked Leads:")
    for lead in ranked:
        print(lead)
