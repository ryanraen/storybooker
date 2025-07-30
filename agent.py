import os
from strands import Agent
from strands.models.openai import OpenAIModel
from strands.tools.mcp import MCPClient
from mcp.client.stdio import stdio_client, StdioServerParameters
from dotenv import load_dotenv

def main():
    print("Connecting to server...")
    mcp_client = MCPClient(lambda: stdio_client(StdioServerParameters(
        # command="uv",
        # args=["run", "mcp", "dev", "mcpserver.py"]
        command="python",
        args=["mcpserver.py"]
    )))

    print("Setting up OpenAI model...")
    load_dotenv()
    model = OpenAIModel(
        client_args={
            "api_key": os.environ.get("OPENAI_API_KEY"),
        },
        model_id="gpt-4.1-nano",
        params={
            "max_tokens": 5000,
            "temperature": 0.7,
        }
    )

    try:
        with mcp_client:
            agent = Agent(
                model=model,
                # System prompt used to test individual tools
                system_prompt="""
                When the user gives a prompt, you must:
                1. Feed the prompt into storyboarder.
                2. Format the result of step 1.
                3. Return ALL raw result of step 2.
                
                After COMPLETELY finishing steps 1-3:
                1. Generate all required base character images and base background images for the story.
                2. Generate all altered character and background images to fit the context in each page.
                """
                
                # SYS INSTRUCTIONS LEFT COMMENTED BELOW TO TESTING INDIVIDUAL TOOLS
                
                # system_prompt="""
                # You are an autonomous agent that generates children's comics based on one user prompt.
                # Your primary role is to be an intelligent orchestrator agent responsible for completing complex tasks by coordinating with external tools.

                # When a user provides a single prompt describing a desired comic book, your goal is the following:
                # 1. Feed the prompt into the storyboarder tool.
                # 2. Return the raw result of step 1.

                # You do not solve sub-tasks yourself. Instead, you use the tools provided to you via the MCP server. Your role is to plan, delegate, and ensure the final output is coherent and complete.

                # Rules:
                # - You must always use, and only use the tools provided to you by the MCP server to complete each sub-task.
                # - You must clearly record each step and result in the context so that other tools and models can refer back to it.
                # - You must respond with "That is outside of my capabilities." when given a task you cannot complete.
                # - You must NOT ask the user for future input.
                # - You must NOT attempt to make up outputs for tools you do not have access to.
                # - You must not invent information or skip required steps in the task.
                # - You should think step-by-step and ensure each tool is used at the appropriate time.
                # - If you need to call a tool multiple times (e.g. for each comic panel), do so in a loop, maintaining memory of earlier results.
                # - Assume that the user prompt defines the overall comic concept and your goal is to return a complete story in comic book form using tools.

                # You are capable of:
                # - Interpreting the user’s comic idea
                # - Breaking the comic into a structured narrative


                # You are not capable of:
                # - Drawing images yourself
                # - Writing longform stories from scratch without using tools
                # - Performing creative tasks not supported by your tools

                # When in doubt, delegate. Your value lies in coordination, not creativity.
                # """
                
                # TEMP REMOVED FROM 'When a user provides a ...':
                # 1. Understand the user's goal.
                # 2. Break it down into steps.
                # 3. Complete each step by calling tools provided via the MCP server.
                # 4. Automatically continue execution through all steps.
                # 5. Return the final result, without requiring the user to prompt again.
                
                # TEMP REMOVED FROM 'You are capable of':
                # - Generating artwork, dialogue, and layout by delegating to tools
                # - Assembling the final comic output (e.g. PDF, web format)
                )
            
            mcp_tools = mcp_client.list_tools_sync()
            print(f"Available tools: {[tool.tool_name for tool in mcp_tools]}")
            
            agent.tool_registry.process_tools(mcp_tools)
            
            while True:
                user_input = input("\nPlease enter a comic story idea.\n")
                
                if user_input.lower() in ["exit", "quit", "bye", "stop"]:
                        print("See you next time!")
                        break
                    
                print("Processing request...")
                
                result = agent(user_input)
                
    except Exception as e:
            print("SERVER CONNECTION FAILED: " + str(e.with_traceback(None)))

