import os
import openai

class OutreachContentAgent:
    """
    OutreachContentAgent:
    Generates personalized outreach emails for ranked leads using OpenAI GPT.
    """

    def __init__(self, openai_api_key=None, model="gpt-4o-mini"):
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_KEY")
        self.model = model
        openai.api_key = self.openai_api_key

    def generate_email(self, lead, persona="SDR", tone="friendly"):
        """
        Generate a personalized email for a single lead.
        """
        prompt = f"""
You are a {persona} writing a {tone} outreach email.

Lead details:
- Name: {lead.get('contact')}
- Company: {lead.get('company')}
- Role: {lead.get('role')}
- Technologies: {', '.join(lead.get('technologies', []))}

Write a concise, personalized email introducing your company, and suggest a next step for a call or demo.
"""
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=250
            )
            email_body = response.choices[0].message.content.strip()
            return email_body
        except Exception as e:
            print(f"[OpenAI API Error]: {e}")
            return "Could not generate email."

    def run(self, ranked_leads, persona="SDR", tone="friendly"):
        """
        Generate emails for all leads.
        """
        messages = []
        for lead in ranked_leads:
            email_body = self.generate_email(lead, persona, tone)
            messages.append({
                "lead": lead.get("email"),
                "email_body": email_body
            })
        return messages


# Example usage
if __name__ == "__main__":
    sample_leads = [
        {
            "company": "Acme Corp",
            "contact": "John Doe",
            "role": "CTO",
            "technologies": ["Python", "AWS"],
            "email": "john.doe@acme.com",
            "score": 1.0
        }
    ]

    agent = OutreachContentAgent()
    messages = agent.run(sample_leads)
    for msg in messages:
        print(msg)
