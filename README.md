# Demo-ready Outbound Lead Generation Workflow

## Aim of the Project
The aim of this project is to **automate end-to-end B2B lead generation**.  
It identifies prospects, enriches their data, ranks leads based on configurable criteria, generates personalized outreach emails, tracks responses, and provides feedback for improving campaigns.  
The workflow is modular, scalable, and can integrate multiple APIs for real-world usage.

---

## Implementation
The workflow is implemented using **modular Python agents**, each responsible for a specific task:

### 1. Prospect Search Agent
- Searches for potential leads based on ideal customer profile (ICP) parameters such as industry, location, employee count, revenue, and business signals.
- Integrates APIs like **Clay** and **Apollo** to fetch leads.

### 2. Data Enrichment Agent
- Enriches leads with additional information such as technologies used, LinkedIn profiles, and verified email addresses.
- Integrates enrichment APIs like **Clearbit** for real-time data.

### 3. Scoring Agent
- Scores leads using configurable criteria: employee count, revenue, role match, and tech stack.
- Ranks leads in descending order to prioritize high-potential prospects.

### 4. Outreach Content Agent
- Generates **personalized outreach emails** using **OpenAI GPT**.
- Emails consider lead details, role, company, and technologies.
- Persona and tone can be customized (e.g., friendly, formal, technical).

### 5. Outreach Executor Agent
- Sends emails to leads (integration with email systems in production).
- Executes the outreach step for campaigns.

### 6. Response Tracker Agent
- Tracks email opens, clicks, replies, and meetings booked for each campaign using APIs like Apollo.
- Provides structured outputs for further analysis.

### 7. Feedback Trainer Agent
- Analyzes campaign responses to generate recommendations for improving emails or targeting.
- Logs feedback to Google Sheets for review and optimization.

The workflow is orchestrated via a **Python script (`langgraph_builder.py`)** that reads a **`workflow.json`** file.  
Each step’s output is passed as input to the next, enabling an **end-to-end automated pipeline**.

---

## Environment Setup (.env)
To run the project, create a `.env` file in the project root and include all required API keys:

```env
# API keys
CLAY_API_KEY=your_clay_api_key
APOLLO_API_KEY=your_apollo_api_key
CLEARBIT_KEY=your_clearbit_key
OPENAI_KEY=your_openai_key
SHEET_ID=your_google_sheet_id
