# AI CCTV Operator
This project holds the code to implement an AI program, responsible for analyzing the cameras from a CCTV, and answering the questions a user has, based on the gathered info

## How to run
Before running the program, please make sure you have configured the following environment variables:
- `LANGCHAIN_API_KEY`: The API key to access the LangChain API
- `OPENAI_API_KEY`: The API key to access the OpenAI API

To run the program, you need to have Python 3.7 installed. Then, you can run the following command:
```bash
python main.py
```

## How to test
Once the program is running, an API will be available at `http://localhost:8080`. You can test the API by sending a POST request to the `/analyze` endpoint, with the following body:
```json
{
    "user_input": "What's happening in my garage?"
}
```
Once the request is sent, the program will identify which are the best cameras to use and will process the images to answer the user's question.
Once completed, the program will return a JSON response, similar to the following:
```json
{
    "result": "Based on the provided image from the garage camera, the situation appears as follows: A car is parked inside the garage. There are bicycles and some furniture or objects stored along the side. The garage door is open, leading to an outdoor area or patio with chairs and a table visible.This observation is based on the footage from Camera 1 in the garage."
}
```
Please note that the response will always include the name of the camera used to gather the information.