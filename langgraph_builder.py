import os
import json
from dotenv import load_dotenv

# Load agents
from agents.prospect_search_agent import ProspectSearchAgent
from agents.data_enrichment_agent import DataEnrichmentAgent
from agents.scoring_agent import ScoringAgent
from agents.outreach_content_agent import OutreachContentAgent
from agents.outreach_executor_agent import OutreachExecutorAgent
from agents.response_tracker_agent import ResponseTrackerAgent
from agents.feedback_trainer_agent import FeedbackTrainerAgent

load_dotenv()

# Load workflow.json
with open("workflow.json") as f:
    workflow = json.load(f)

# Dictionary to store outputs of each step
outputs = {}

# Mapping agent names to classes
AGENT_CLASSES = {
    "ProspectSearchAgent": ProspectSearchAgent,
    "DataEnrichmentAgent": DataEnrichmentAgent,
    "ScoringAgent": ScoringAgent,
    "OutreachContentAgent": OutreachContentAgent,
    "OutreachExecutorAgent": OutreachExecutorAgent,
    "ResponseTrackerAgent": ResponseTrackerAgent,
    "FeedbackTrainerAgent": FeedbackTrainerAgent
}

def replace_placeholders(obj, outputs):
    """
    Recursively replace {{step.output.key}} with actual data from previous step outputs
    """
    if isinstance(obj, dict):
        return {k: replace_placeholders(v, outputs) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_placeholders(item, outputs) for item in obj]
    elif isinstance(obj, str) and obj.startswith("{{") and obj.endswith("}}"):
        ref = obj[2:-2].strip()
        # Example: prospect_search.output.leads
        parts = ref.split(".")
        data = outputs
        for part in parts:
            data = data.get(part, {})
        return data
    else:
        return obj

def main():
    for step in workflow["steps"]:
        agent_name = step["agent"]
        AgentClass = AGENT_CLASSES.get(agent_name)

        print(f"\n=== Running Step: {step['id']} ({agent_name}) ===")

        inputs = replace_placeholders(step.get("inputs", {}), outputs)

        # Instantiate agent with relevant API keys
        if agent_name == "ProspectSearchAgent":
            agent = AgentClass(
                clay_api_key=os.getenv("CLAY_API_KEY"),
                apollo_api_key=os.getenv("APOLLO_API_KEY")
            )
            result = agent.run(**inputs)

        elif agent_name == "DataEnrichmentAgent":
            agent = AgentClass(pdl_api_key=os.getenv("PDL_API_KEY"))
            result = agent.run(inputs.get("leads", []))

        elif agent_name == "ScoringAgent":
            agent = AgentClass(scoring_criteria=workflow.get("config", {}).get("scoring", {}))
            result = agent.run(inputs.get("enriched_leads", []))

        elif agent_name == "OutreachContentAgent":
            agent = AgentClass(openai_api_key=os.getenv("OPENAI_KEY"))
            result = agent.run(
                ranked_leads=inputs.get("ranked_leads", []),
                persona=inputs.get("persona", "SDR"),
                tone=inputs.get("tone", "friendly")
            )

        elif agent_name == "OutreachExecutorAgent":
            agent = AgentClass(apollo_api_key=os.getenv("APOLLO_API_KEY"))
            result = agent.run(inputs.get("messages", []))

        elif agent_name == "ResponseTrackerAgent":
            agent = AgentClass(apollo_api_key=os.getenv("APOLLO_API_KEY"))
            # Extract campaign IDs from previous step
            campaign_ids = [item.get("campaign_id") for item in inputs.get("campaign_id", []) if item.get("campaign_id")]
            result = agent.run(campaign_ids)

        elif agent_name == "FeedbackTrainerAgent":
            agent = AgentClass(sheet_id=os.getenv("SHEET_ID"))
            result = agent.run(inputs.get("responses", []))

        else:
            print(f"Unknown agent: {agent_name}")
            continue

        outputs[step["id"]] = {"output": result}
        print(f"Step {step['id']} completed. Output: {str(result)[:200]}...")  # Print first 200 chars

    print("\n=== Workflow Completed ===")
    return outputs


if __name__ == "__main__":
    main()
