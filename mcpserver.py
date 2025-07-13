import os
from mcp.server import FastMCP
from strands import tool
from openai import OpenAI
from dotenv import load_dotenv
import json

# CONSTANTS
AI_MODEL_ID = "gpt-4.1-nano"

# Initialize MCP Server entity
mcp = FastMCP(name="MCP Server",
              stateless_http=False)

# Load env vars
load_dotenv()

# Create OpenAI client
ai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


# SERVER TOOLS

@mcp.tool()
def storyboarder(prompt: str) -> dict:
    """
    Given requirements for a children's story, generates a 6-panel comic storyboard plan that satisfies provided demands
    Input: user prompt requirements for a story
    Output: python dictionary of 6 panels as such:
        [
          {{"title": "...", 
            "summary": "...", 
            "characters": ["..."], 
            "setting": "...", 
            "dialogue": [{"speaker": "...", "line": "..."}, ...]}},
          ...
        ]
    """
    
    # Prompt LLM for storyboard plan
    response = ai_client.responses.create(
        model=AI_MODEL_ID,
        instructions="""
        You are a children's storyteller who structures comics in 6 panels.
        Based on the user prompted story idea, create a structured 6-panel comic storyboard.

        Rules:
        1. Each panel should include 
            - title: short (max 6 words)
            - summary: what happens in that panel
            - characters: list of character names in that panel
            - setting: brief physical description
            - dialogue: list of short exchanges (max 3)
        2. Keep it engaging and age-appropriate.
        3. Return it as a JSON list of 6 panels like this:
                [
                {{"title": "...", 
                  "summary": "...", 
                  "characters": ["..."], 
                  "setting": "...", 
                  "dialogue": [{"speaker": "...", "line": "..."}, ...]}},
                ...
                ]
        """,
        input=prompt
    )
    
    # Returns LLM output JSON as dict
    return json.loads(response.output_text)

@mcp.tool()
def image_gen(characters: list, bg_scenes: list) -> dict:
    pass

# Run MCP server locally
mcp.run(transport="streamable-http")