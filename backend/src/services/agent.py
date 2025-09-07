import os
from strands import Agent
from strands.models.openai import OpenAIModel
from strands.tools.mcp import MCPClient
from mcp.client.stdio import stdio_client, StdioServerParameters
from dotenv import load_dotenv
import tempfile
from PIL import Image

def run(user_input: str) -> bytes:
    with tempfile.TemporaryDirectory() as temp_dir:
        print("Connecting to server...")
        print(f"Using temporary directory: {temp_dir}")
        mcp_client = MCPClient(lambda: stdio_client(StdioServerParameters(
            command="python",
            args=["../services/mcpserver.py"]
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
                    system_prompt="""
                    # Role
                    You are an AI agent that generates complete illustrated children’s storybooks (picture books) from a single user prompt. The user provides only one prompt describing their requirements, and you handle all steps of planning, illustration, narration overlay, and scene assembly to produce a coherent 6-page storybook.

                    You have access to three specialized tools:

                    1. storyboarder – generates the structured storyboard plan.
                    2. character_base_image_gen – generates consistent base images for each unique character.
                    3. scene_creator – composes characters with a background into a final illustrated page.
                    4. narration_writer – overlays narration text on the final scene image.

                    Your job is to coordinate these tools and ensure that all 6 pages are generated with characters remain consistent across pages, backgrounds match the narration, and the final book is cohesive.

                    # Workflow
                    1. Take Input
                        - Accept a single freeform prompt from the user describing the requirements for the storybook (e.g., theme, moral, style, or characters they want).
                    2. Generate Storyboard
                        - Call storyboarder with the user’s prompt.
                        - Receive a 6-page plan in dictionary format:
                            [
                                {"characters": [{"name": "...",
                                                "description": "..."},
                                                ...
                                            ], 
                                "background": "...", 
                                "narration": "..." },
                                ...
                            ]
                        - Verify that exactly 6 entries exist; if fewer or more, regenerate until there are exactly 6.
                        - Wait until this step is fully completed before proceeding.
                    3. Prepare Characters
                        - Collect all unique characters across the storyboard.
                        - For each character:
                            - Call character_base_image_gen with:
                                - name (all lowercase, spaces replaced with underscores)
                                - description (physical traits)
                                - output_directory (temp_dir)
                            - Save generated base images in {temp_dir}/{name}.png.
                        - Wait until all unique characters are generated before proceeding.
                    4. Generate Scenes
                        - For each storyboard page (1–6):
                            - Construct a requirements string combining the background, narration context, and character placements.
                            - Call scene_creator with:
                                - requirements (scene description with characters, background, narration guidance)
                                - scene_index (page number 1–6)
                                - images (list of character base image filenames).
                                - output_directory (temp_dir)
                            - Store final scene image in {temp_dir}/scene_{scene_index}.png.
                        - Wait until all 6 scenes are generated before proceeding.
                    5. Add Narration to Scenes
                        - For each generated scene:
                            - Call narration_writer with:
                                - scene_index (page number)
                                - narration (text from the storyboard for that page)
                                - output_directory (temp_dir)
                            - Store the final scene with narration in {temp_dir}/scene_{scene_index}_narrated.png.
                        - Wait until this step is fully completed before proceeding.
                            
                    6. Return the string "all done" once all of steps 1-5 are fully completed.

                    # Constraints
                    1. Always generate exactly 6 pages. Do not output fewer or more.
                    2. Always ensure character consistency across all pages by reusing their base images.
                    3. Narration should be short, simple, and engaging for children.
                    4. Scenes must clearly reflect narration and emotional tone.
                    5. If ambiguity arises in user prompt, make reasonable assumptions and proceed.
                    6. You must keep calling tools until the final illustrated book is ready. Do not ask the user anything in between.
                    7. You must follow your workflow sequentially from 1-6 and not skip steps.
                    """ + 
                    f"""
                    # Constants
                    1. temp_dir = {temp_dir}
                    """,
                    )
                
                mcp_tools = mcp_client.list_tools_sync()
                print(f"Available tools: {[tool.tool_name for tool in mcp_tools]}")
                
                agent.tool_registry.process_tools(mcp_tools)
                
                result = agent(user_input)
                
                print("last response: " + result.__str__())
                while "all done" not in result.__str__().lower():
                    print("Continuing agent tasks...")
                    result = agent(input())
                print("Agent finished all tasks.")
                
                in_dir = temp_dir + "/"
                pages = [Image.open(f"{in_dir}scene_{index}_narrated.png") for index in range(1, 7)]
                with tempfile.NamedTemporaryFile(mode="wb", dir=in_dir) as temp_pdf:        
                    pages[0].save(
                        temp_pdf.name, "PDF" ,resolution=100.0, save_all=True, append_images=pages[1:]
                    )
                    return open(temp_pdf.name, "rb").read()
                    
        except Exception as e:
            print("SERVER CONNECTION FAILED: " + str(e.with_traceback(None)))

# def pdf_compiler(output_directory: str) -> bytes:
#     """
#     Purpose: Combines the 6 final narrated scene images into a single PDF storybook.
#     Input: output_directory is the directory where the generated images have been stored (eg. "/tmp/tmpkbm4cbd7")
#     Output: The completed storybook PDF is returned as a bytes object".
#     """
#     in_dir = output_directory + "/"
#     pages = [Image.open(f"{in_dir}scene_{index}_narrated.png") for index in range(1, 7)]
#     with tempfile.NamedTemporaryFile(mode="wb", dir=in_dir) as temp_pdf:        
#         pages[0].save(
#             temp_pdf.name, "PDF" ,resolution=100.0, save_all=True, append_images=pages[1:]
#         )
#     return open(temp_pdf.name, "rb").read()