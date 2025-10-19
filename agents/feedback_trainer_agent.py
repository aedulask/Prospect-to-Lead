class FeedbackTrainerAgent:
    """
    Demo-ready FeedbackTrainerAgent:
    Analyzes campaign responses and prints recommendations to console.
    Does NOT require Google Sheets or credentials.
    """

    def __init__(self):
        print("[FeedbackTrainerAgent] Running in demo mode (no Google Sheets).")

    def analyze_responses(self, responses):
        """
        Analyze open, click, reply rates and generate simple recommendations.
        """
        if not responses:
            return ["No responses to analyze."]

        from statistics import mean

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

    def run(self, responses):
        """
        Main method: analyze responses and print recommendations.
        """
        recommendations = self.analyze_responses(responses)
        for rec in recommendations:
            print(f"[FeedbackTrainerAgent] Recommendation: {rec}")
        return recommendations


# Demo run
if __name__ == "__main__":
    sample_responses = [
        {"lead": "john@acme.com", "opened": True, "clicked": False, "replied": False},
        {"lead": "jane@beta.com", "opened": True, "clicked": True, "replied": True},
        {"lead": "mark@xyz.com", "opened": False, "clicked": False, "replied": False}
    ]

    agent = FeedbackTrainerAgent()
    recommendations = agent.run(sample_responses)

    print("\n[FeedbackTrainerAgent] Final Recommendations:")
    for r in recommendations:
        print(r)
