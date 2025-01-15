import os
import requests
from datetime import datetime
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI 
from langgraph.graph import START, END, StateGraph

import daily_brew.configuration as configuration
from daily_brew.state import State, Brew

def make_brew(state: State, config: RunnableConfig):
    """Generate the daily brew 

    Args:
        state (State): State 
        config (RunnableConfig): Configuration object

    Returns:
        dict: Updated state with the daily brew
    """

    # Get the configuration
    configurable = configuration.Configuration.from_runnable_config(config)
    model = configurable.model
    DAILY_BREW_PROMPT = configurable.DAILY_BREW_PROMPT

    # Format prompt and run model 
    instructions = DAILY_BREW_PROMPT.format(time=datetime.now().isoformat())
    llm = ChatOpenAI(model=model).with_structured_output(Brew) 
    brew = llm.invoke(instructions)

    # Update state with the daily brew
    return {"brew": brew} 

def write_to_slack(state: State):
    """Generate the daily brew 

    Args:
        state (State): State 

    Returns:
        None
    """
    
    # Full set of interview reports
    brew = state.brew

    # Write to your Slack Channel via webhook
    true = True
    headers = {
        'Content-Type': 'application/json',
    }

    # Blocks
    blocks = []
    
    # Block 1: Title section
    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"*{brew.title}*"
        }
    })
    
    # Block 2: Divider
    blocks.append({
        "type": "divider"
    })
    
    # Block 3: Content section
    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"{brew.brew}"
        }
    })

    # Block 4: Divider
    blocks.append({
        "type": "divider"
    })
    
    blocks.insert(0, {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": ":coffee: o1 is brewing ...",
            "emoji": true
        }
    })
    
    data = {
        "blocks": blocks,
        "unfurl_links": True,
        "unfurl_media": True,
    }
    
    response = requests.post(os.getenv("SLACK_WEBHOOK"), headers=headers, json=data)

# Create the graph + all nodes
builder = StateGraph(State, config_schema=configuration.Configuration)
builder.add_node("make_brew",make_brew)
builder.add_node("write_to_slack",write_to_slack)
builder.add_edge(START, "make_brew")
builder.add_edge("make_brew", "write_to_slack")
builder.add_edge("write_to_slack", END)

# Compile the graph
graph = builder.compile()