import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from statistics import mean

class FeedbackTrainerAgent:
    """
    FeedbackTrainerAgent:
    Analyzes campaign responses and suggests improvements to the outreach workflow.
    Stores recommendations in Google Sheets.
    """

    def __init__(self, sheet_id=None, creds_json_path="google_service_account.json"):
        self.sheet_id = sheet_id or os.getenv("SHEET_ID")
        self.creds_json_path = creds_json_path
        self.gc = self.authenticate()
        self.sheet = self.gc.open_by_key(self.sheet_id).sheet1

    def authenticate(self):
        """
        Authenticate with Google Sheets API using service account.
        """
        scope = ['https://spreadsheets.google.com/feeds', 
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.creds_json_path, scope)
        client = gspread.authorize(creds)
        return client

    def analyze_responses(self, responses):
        """
        Analyze open, click, reply rates and generate simple recommendations.
        """
        if not responses:
            return ["No responses to analyze."]

        open_rate = mean([r.get("opened", 0) for r in responses]) * 100
        click_rate = mean([r.get("clicked", 0) for r in responses]) * 100
        reply_rate = mean([r.get("replied", 0) for r in responses]) * 100

        recommendations = []

        if open_rate < 20:
            recommendations.append("Consider improving email subject lines to increase opens.")
        if click_rate < 10:
            recommendations.append("Include clearer CTA or links to increase clicks.")
        if reply_rate < 5:
            recommendations.append("Personalize emails further or adjust targeting (ICP).")
        if reply_rate >= 5:
            recommendations.append("Current approach is effective, continue testing variations.")

        return recommendations

    def log_to_sheet(self, recommendations):
        """
        Log recommendations to Google Sheets.
        """
        for rec in recommendations:
            self.sheet.append_row([rec])

    def run(self, responses):
        """
        Main method: analyze responses and log recommendations.
        Returns list of recommendations.
        """
        recommendations = self.analyze_responses(responses)
        self.log_to_sheet(recommendations)
        return recommendations


# Example usage
if __name__ == "__main__":
    sample_responses = [
        {"lead": "john@acme.com", "opened": True, "clicked": False, "replied": False},
        {"lead": "jane@beta.com", "opened": True, "clicked": True, "replied": True},
        {"lead": "mark@xyz.com", "opened": False, "clicked": False, "replied": False}
    ]

    agent = FeedbackTrainerAgent(sheet_id="your_google_sheet_id")
    recommendations = agent.run(sample_responses)
    for r in recommendations:
        print(r)
