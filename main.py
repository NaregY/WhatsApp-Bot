# Third-party imports
import os
import openai
from fastapi import FastAPI, Form, Request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from utils import send_message, logger
from fastapi.responses import PlainTextResponse

app = FastAPI()
load_dotenv()

# Set up the OpenAI API client
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/")
async def index():
    return {"msg": "working"}

@app.post("/message")
async def reply(request: Request, Body: str = Form()):
    # Call the OpenAI API to generate text with ChatGPT
    messages = [{"role": "user", "content": Body}]
    messages.append({"role": "system", "content": "You're an investor, a serial founder and you've sold many startups. You understand nothing but business."})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.5
    )

    # The generated text
    chatgpt_response = response.choices[0].message.content

    # Create the TwiML response
    twiml_response = f"<Response><Message>{chatgpt_response}</Message></Response>"

    # Return the TwiML response with the appropriate Content-Type header
    return PlainTextResponse(content=twiml_response, media_type="application/xml")

    # Send the response back to the user using Twilio
    response = MessagingResponse()
    response.message(chatgpt_response)

    # Send the Twilio response
    return str(response)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
