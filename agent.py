import os
from strands import Agent, tool
from strands.models.openai import OpenAIModel
from strands.tools.mcp import MCPClient
from mcp.client.streamable_http import streamablehttp_client
from dotenv import load_dotenv

def main():
    
    # Connect to MCP Server
    print("Connecting to server...")
    mcp_server = MCPClient(lambda: streamablehttp_client("http://127.0.0.1:8000/mcp"))

    # OPENAI MODEL SPEC
    print("Setting up OpenAI model...")
    load_dotenv() # load env vars
    model = OpenAIModel(
        client_args={
            "api_key": os.environ.get("OPENAI_API_KEY"),
        },
        # **model_config
        model_id="gpt-4.1-nano",
        params={
            "max_tokens": 1000,
            "temperature": 0.7,
        }
    )


    try:
        with mcp_server:
            
            # Create agent
            agent = Agent(
                model=model,
                system_prompt=
                "You are a helpful assistant for completing simple tasks."
                
                "When a user requests a task to be completed, \
                answer as simply and concisely as possible while fully completing the given task."
                
                "Rules:"
                "- You must use the tools provided to you by the MCP server."
                "- You must respond with \"That is outside of my capabilities.\" when given a task you cannot complete."
                "- You must NOT make up your own answers to tasks outside of your ability."
            )
            
            # List tools available on the MCP server
            mcp_tools = mcp_server.list_tools_sync()
            print(f"Available tools: {[tool.tool_name for tool in mcp_tools]}")

            # add them to the agent
            agent.tool_registry.process_tools(mcp_tools)
            
            while True:
                user_input = input("\nPlease enter a task to be completed by the LLM.\n")
                
                if user_input.lower() in ["exit", "quit", "bye", "stop"]:
                        print("See you next time!")
                        break
                    
                print("Processing request...")
                
                result = agent(user_input)
                
    except Exception as e:
            print("SERVER CONNECTION FAILED: " + e)

