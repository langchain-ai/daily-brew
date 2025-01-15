# 🤖 o1 Daily Brew ☕

o1 Daily Brew is a daily reflection from o1 published to a Slack channel of your choice.

## Quick Start

1. Clone the repo.

2. Create a Slack app and add your webhook URL to your environment variable `SLACK_WEBHOOK`(see below).

3. Create a [LangGraph Platform deployment](https://langchain-ai.github.io/langgraph/concepts/deployment_options/). 

> Any [paid LangSmith plan](https://www.langchain.com/pricing-langsmith) has access to LangGraph Platform and deployments.

4. Create a [cron job](https://langchain-ai.github.io/langgraph/cloud/how-tos/cron_jobs/) to run the deployment at your desired time. 

```python 
from langgraph_sdk import get_client

# URL from our LangGraph Cloud deployment
url = "deployment_url"
client = get_client(url=url)

# An assistant ID is automatically created for each deployment
await client.assistants.search(metadata={"created_by": "system"})

# Use the SDK to schedule a cron job to run at 11:00 AM PST (19:00 UTC) every day
cron_job_stateless = await client.crons.create(
    your_assistant_id,
    schedule="0 19 * * *",
    input={"user_provided_topics": "AI"} 
)
```

## Slack

Create a Slack app to publish to Slack.

1. Go to https://api.slack.com/apps
2. Click "Create New App"
3. Choose "From scratch"
4. Name your app (e.g., "o1 Daily Brew") and select your workspace
5. Once created, go to "Incoming Webhooks" in the left sidebar
6. Toggle "Activate Incoming Webhooks" to On
7. Click "Add New Webhook to Workspace"
8. Choose the channel where you want the messages to appear
9. Copy the "Webhook URL" that's generated

Add add webhook URL credentials to your environment variable `SLACK_WEBHOOK`. 