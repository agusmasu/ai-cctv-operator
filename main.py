from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
import os
import base64
import json

from camera import Camera, get_user_cameras
from stream.steramprovider import MockedStreamProvider

# Set environment variables
os.environ["LANGCHAIN_TRACING_V2"] = "true"

app = FastAPI()


# Define input model for the request
class CameraAnalysisRequest(BaseModel):
    user_input: str


# Define response model
class CameraAnalysisResponse(BaseModel):
    result: str


# FastAPI endpoint for analyzing cameras
@app.post("/analyze", response_model=CameraAnalysisResponse)
async def analyze_cameras(request: CameraAnalysisRequest):
    global image_prompt_messages
    user_input = request.user_input

    # Get current configured cameras
    user_cameras = get_user_cameras()

    # Encode example image to base64 for mocked frames
    with open("IMG_WITH_NO_PERSON.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

    # Initialize model
    model = ChatOpenAI(model="gpt-4o")

    # Prompt template for camera selection and filtering
    camera_selection_prompt = PromptTemplate.from_template(
        """
        You are given a list of cameras and their features in JSON format.
        Based on the user's prompt, select the cameras that best match the description and return them as a JSON array,
        with each entry containing the camera's complete info. Use all cameras in case of no specific selection.

        User Prompt: "{user_input}"
        Cameras: {camera_data}

        Your Response (JSON format):
        """
    )

    # Convert camera data to JSON format
    cameras_json = json.dumps([camera.to_json() for camera in user_cameras])

    # Camera selection step
    camera_selection_chain = camera_selection_prompt | model | JsonOutputParser()

    # Invoke the camera selection
    selected_cameras = camera_selection_chain.invoke({
        "user_input": user_input,
        "camera_data": cameras_json
    })

    # Collect base64-encoded image data for only the selected cameras
    prompt_images = []
    for camera in selected_cameras:
        # Mocked frame provider usage for each selected camera
        frame_provider = MockedStreamProvider(image_content=encoded_string)
        frame = frame_provider.get_current_stream_frame(Camera(**camera))  # Using the camera object
        prompt_images.append(frame)

    # Define the prompt with both camera selection and image analysis
    system_messages = [{"type": "text", "text": "You are an expert in analyzing camera footage."}]

    user_messages = [{"type": "text", "text":
        "Based on the security footage from the selected cameras, answer the following question: {user_input}."
        "Please include which cameras you've used to make your answer."
        "These are the securtty cameras provided (in order: {selected_cameras})"}]

    # Add each image URL to the prompt messages
    for img in prompt_images:
        user_messages.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img}"}})

    # Build the final ChatPromptTemplate
    final_prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_messages),
        ("user", user_messages)
    ])

    # Create the final chain with the structured prompt template and output parser
    final_chain = final_prompt_template | model | StrOutputParser()
    response = final_chain.invoke({"user_input": user_input, "selected_cameras": selected_cameras})

    # Return the response as JSON
    return CameraAnalysisResponse(result=response)


# Run the app with: uvicorn main:app --reload

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
