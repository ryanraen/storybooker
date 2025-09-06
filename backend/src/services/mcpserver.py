import os
import tempfile
from mcp.server import FastMCP
from openai import OpenAI
from dotenv import load_dotenv
import json
from PIL import Image
from google import genai
from google.genai.types import (
    HttpOptions,
)
import base64
import cv2
import textwrap

OPENAI_MODEL_ID = "gpt-4.1-nano" # "gpt-4.1"
IMAGEN_MODEL_ID = "imagen-3.0-fast-generate-001" # "imagen-3.0-generate-002"
PAGE_SIZE = "1024x1024"

load_dotenv()
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
gcloud_client = genai.Client(http_options=HttpOptions(api_version="v1"),
                      vertexai=os.environ.get("GOOGLE_GENAI_USE_VERTEXAI"),
                      project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
                      location=os.environ.get("GOOGLE_CLOUD_LOCATION"))

mcp = FastMCP(name="MCP Server",
              stateless_http=False)

temp_dir = tempfile.TemporaryDirectory()

@mcp.tool()
def storyboarder(prompt: str) -> dict:
    """
    Purpose: Given requirements for a children's story book, generates a 6 page storyboard plan that satisfies provided demands
    Input: user prompt requirements for a story
    Output: python dictionary of 6 pages as such:
        [
          { "characters": [{"name": "...",
                            "description": "..."},
                            ...
                            ], 
            "background": "...", 
            "narration": "..." },
          ...
        ]
    """
    response = openai_client.responses.create(
        model=OPENAI_MODEL_ID,
        instructions="""
        You are a children's storyteller who structures story books in 6 pages.
        Based on the user prompted story idea, create a structured 6-page storyboard.

        Rules:
        1. Each page should include 
            - characters: list of character names in that panel and physical description of the character (eg. name: "Peppa Pig"; description: "pig, red shirt, happy, green shoes")
            - background: point form physical description of the background scene (eg. "grass field, sunny, clouds, sparse trees, house in the distance")
            - narration: one line that the narrator should say
        2. Keep it engaging and age-appropriate.
        3. Return it as a JSON list of 6 panels like this:
            [
                {"characters": [{"name": "...",
                                 "description": "..."},
                                 ...
                               ], 
                 "background": "...", 
                 "narration": "..." },
                ...
            ]
        """,
        input=prompt
    )
    return json.loads(response.output_text)

@mcp.tool()
def character_base_image_gen(name: str, description: str, output_directory: str) -> str:
    """
    Purpose: Given physical descriptions of a character, generates a base image for it
    Input: name is the name of the character in all lower case (eg. peppa pig); 
           description is the additional specified physical traits of the character being generated (eg. "pig, red shirt, happy, green shoes").
           output_directory is the directory where the generated image should be stored (eg. "/tmp/tmpkbm4cbd7")
    Output: the generated image is stored in "{output_directory}/base/" as "{name}.png" where any spaces in name are replaced with underscores.
    """
    out_dir = output_directory + "/base/"
    
    traits = gcloud_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            f"""
            Return a specific set of defining physical traits for a children's cartoon character with:
            name: "{name}",
            additional description: "{description}"
            
            Example output for a character like "Peppa Pig":
            
            The character in the image is a stylized, pink pig-like figure, standing upright and facing forwards.
            Here are its defining physical traits, with emphasis on direction:
            *   **Head and Face:**
                *   The head is large and distinctly pink, facing forwards, with the snout protruding forward.
                *   Two large, white, circular eyes with small black pupils are visible on the upper part of the face, both looking forward.
                *   A prominent, darker pink, oval-shaped snout extends forward from the center of the face, with two smaller, darker pink oval nostrils positioned vertically on its front side.
                *   A single, darker pink, circular blush mark is located on the left cheek of the face.
                *   A simple, downward-curving sad mouth in a darker pink hue is drawn below the eyes and centrally below the snout.
                *   Two small, pointed, light pink ears are positioned at the top of the head, one slightly to the left and the other slightly to the right, both pointing upward.
            *   **Body and Clothing:**
                *   The body is covered by a solid red dress or tunic, outlined in a darker red.
                *   The dress is bell-shaped, wider at the bottom and tapering upward towards the neck.
            *   **Limbs and Tail:**
                *   Two thin, pink arms extend outward from the sides of the dress, each ending in a stylized hand with three short digits. The left arm is raised and points sharply to the left of the screen, and the right arm extends rightward and slightly downward.
                *   Two thin, pink legs extend downward from beneath the dress, ending in small, flat black shoes or hooves positioned flat on the ground and pointing forward.
                *   A small, curly, pink pig tail protrudes from the lower left side of the character's body, just above the hem of the dress, curling upward and inward.
            """,
        ],
    ).text
    base_img = gcloud_client.models.generate_images(
        model=IMAGEN_MODEL_ID,
        prompt="Style: children's cartoon book\n" + traits
    )
    base_img.generated_images[0].image.save(out_dir + name.replace(" ", "_") + ".png")
    
    return "Tool executed successfully."

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

@mcp.tool()
def scene_creator(scene_index: int, requirements: str, images: list, output_directory: str) -> str:
    """
    Purpose: Given requirements for a scene in the story book, generates one image for it.
    Input: requirements is the text requirement prompt for generating the scene image, 
           eg. "background is a grass field with some trees; character in pose.png is standing on the left side, looking right, happy, pointing right; character in pose3.png is standing on the right, looking left, sad, jumping."
           scene_index is the page number of the scene being generated
           images is a list of the file names of the characters appearing in the scene,
           eg. ["peppa_pig.png", "george.png", ...]
           output_directory is the directory where the generated scene image should be stored (eg. "/tmp/tmpkbm4cbd7")
    Output: Generated scene image is stored as "scene_{scene_index}.png" in "{output_directory}/scene/"
    """
    out_dir = output_directory + "/scene/"
    
    base64_images = [encode_image("backend/res/base/" + path) for path in images]
        
    request_content = [
        {"type": "input_text", "text": requirements},
        ]
    for b64_entry in base64_images:
        request_content.append({"type": "input_image",
                                "image_url": f"data:image/jpeg;base64,{b64_entry}",})
    
    response = openai_client.responses.create(
        model=OPENAI_MODEL_ID,
        input=[
            {
                "role": "user",
                "content": request_content,
            }
        ],
        tools=[{"type": "image_generation", "quality": "high", "size": PAGE_SIZE}],
    )
    
    image_data = [
        output.result for output in response.output
        if output.type == "image_generation_call"
    ]

    if image_data:
        image_base64 = image_data[0]
        with open(f"{out_dir}scene_{scene_index}.png", "wb") as f:
            f.write(base64.b64decode(image_base64))
            
    return "Tool executed successfully."

@mcp.tool()
def narration_writer(scene_index: int, narration: str, output_directory: str) -> str:
    """
    Purpose: Given the page number and narration of the scene, overlays the narration text on the scene image
    Input: scene_index is the page number of the scene being modified
           narration is the narration text that should be added to the scene
           output_directory is the directory where the modified image should be stored (eg. "/tmp/tmpkbm4cbd7")
    Output: Modified scene image is stored as "scene_{scene_index}.png" in "{output_directory}/pages/"
    """
    in_dir = output_directory + "/scene/"
    out_dir = output_directory + "/pages/"

    image = cv2.imread(in_dir + f"scene_{scene_index}.png")
    img_height, img_width, img_channels = image.shape
    wrapped_text = textwrap.wrap(text=narration, width=50)

    font = cv2.FONT_HERSHEY_COMPLEX

    font_size = 1

    outline_color = (0, 0, 0)
    font_color = (255, 255, 255)

    font_thickness = 2
    outline_thickness = 6

    for i, line in enumerate(wrapped_text):
        textsize = cv2.getTextSize(line, font, font_size, font_thickness)[0]

        text_width = textsize[0]
        text_height = textsize[1]

        gap = text_height + 10
        starting_y = int(img_height - gap - len(wrapped_text)*gap)

        y = starting_y + i * gap
        x = int((img_width - text_width) / 2)
        
        # outline
        cv2.putText(image, line, (x, y), font,
                    font_size, 
                    outline_color, 
                    outline_thickness, 
                    lineType = cv2.LINE_AA)
        
        # text
        cv2.putText(image, line, (x, y), font,
                    font_size, 
                    font_color, 
                    font_thickness, 
                    lineType = cv2.LINE_AA)

    cv2.imwrite(out_dir + f"scene_{scene_index}.png", image)
    
# @mcp.tool()
# def pdf_compiler(title: str, output_directory: str) -> str:
#     """
#     Purpose: Combines the 6 final narrated scene images into a single PDF storybook.
#     Input: title is a short and brief title for the final completed storybook
#            output_directory is the directory where the generated images have been stored (eg. "/tmp/tmpkbm4cbd7")
#     Output: The completed storybook PDF is stored as "{output_directory}/final/{title in all lowercase with all " " replaced with "_"}.pdf".
#     """
#     in_dir = output_directory + "/pages/"
#     out_dir = output_directory + "/final/"
#     out_filename = title.lower().replace(" ", "_")
#     pages = [Image.open(f"{in_dir}scene_{index}.png") for index in range(1, 7)]
#     pages[0].save(
#         out_dir + out_filename + ".pdf", "PDF" ,resolution=100.0, save_all=True, append_images=pages[1:]
#     )
    
mcp.run(transport="stdio")