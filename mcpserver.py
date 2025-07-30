import os
from mcp.server import FastMCP
from openai import OpenAI
from dotenv import load_dotenv
import json
from PIL import Image as PImg
from google import genai
from google.genai.types import (
    RawReferenceImage, 
    MaskReferenceImage, 
    MaskReferenceConfig, 
    EditImageConfig, 
    GenerateImagesConfig,
    Image,
    Part,
    HttpOptions,
    ControlReferenceConfig,
    ControlReferenceImage,
    SubjectReferenceConfig,
    SubjectReferenceImage
)

# CONSTANTS
AI_MODEL_ID = "gpt-4.1-nano"

load_dotenv()
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
gcloud_client = genai.Client(http_options=HttpOptions(api_version="v1"),
                      vertexai=os.environ.get("GOOGLE_GENAI_USE_VERTEXAI"),
                      project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
                      location=os.environ.get("GOOGLE_CLOUD_LOCATION"))

mcp = FastMCP(name="MCP Server",
              stateless_http=False)

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
        model=AI_MODEL_ID,
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
def character_base_image_gen(name: str, description: str) -> str:
    """
    Purpose: Given the physical description of a character, generates a base image for it
    Input: name is the name of the character in all lower case (eg. peppa pig); 
           description is the additional specified physical traits of the character being generated (eg. "pig, red shirt, happy, green shoes").
    Output: returns a string of specific set of defining physical traits for the character generated based on the given arguments,
            and the generated image is stored in "./res/base/" as "{name}.png" where any spaces in name are replaced with underscores.
    """
    
    out_dir = "res/base/"
    
    traits = gcloud_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            f"""
            Return a specific set of defining physical traits for a character with:
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
        model="imagen-3.0-generate-002",
        prompt=traits
    )
    base_img.generated_images[0].image.save(out_dir + name.replace(" ", "_") + ".png")
    return traits

@mcp.tool()
def background_scene_image_gen(scene: int, description: str) -> str:
    """
    Purpose: Given the scene index and physical description of a background scene, generates a base image for it
    Input: scene is the page index number that the resulting background image belongs to;
           description is the physical traits of the background being generated (eg. "grass field, sunny, clouds, sparse trees, house in the distance").
    Output: returns a string of specific set of defining physical traits for the background tree generated based on the given arguments,
            and the generated image is stored in "./res/base/" as "bg_{scene}.png".
    """
    
    out_dir = "res/base/"
    
    traits = gcloud_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            f"""
            Return a specific set of defining physical traits for a background scene with:
            description: "{description}"
            """,
        ],
    ).text
    base_img = gcloud_client.models.generate_images(
        model="imagen-3.0-generate-002",
        prompt=traits
    )
    base_img.generated_images[0].image.save(out_dir + "bg_" + scene + ".png")
    return traits

@mcp.tool()
def altered_character_image_gen(name: str, scene: int, traits: str, desired_traits: str) -> None:
    """
    Purpose: Given the name, specific predefined traits, and belonging scene of a character, and the desired traits, generates a new image that alters the base character image to have the desired traits such that the character fits the story/scene.
    Input: name is the name of the character in all lowercase (eg. "peppa pig");
           scene is the page index number that the resulting character image belongs to;
           traits is the specific set of defining physical traits for the given character previously returned by character_base_image_gen;
           desired_traits is the physical traits such as expression, facing direction, pose, emotions that the new altered character image should have (eg. "facing right of screen, hands extending upwards, expression happy")
    Output: the generated altered image is stored in "./res/altered/" as "{name}_{scene}.png" where any spaces in name are replaced with underscores.
    """
    
    out_dir = "res/altered/"
    
    changed_traits = gcloud_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            f"""
            Change and return the following characteristics description such that the character is "{desired_traits}":
            {traits}
            
            Rules:
            -Make as little alterations as possible to achieve ALL the desired changes
            -Emphasize the direction of the character in the description
            -Return just the new characteristics description string
            """
        ],
    ).text

    print(f"\n\nChanged traits: {changed_traits}")

    pose_control_img = gcloud_client.models.generate_images(
        model="imagen-3.0-generate-002",
        prompt=changed_traits
    )

    pose_control_img.generated_images[0].image.save(out_dir + name.replace(" ", "_") + "_" + scene + ".png")


mcp.run(transport="stdio")