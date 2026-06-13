import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

while True:
    prompt = input("how can I help you? ")
    if prompt == "quit":
        break
    else:
        response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = [{"role": "system" , "content": "A financial adviser who has 20 years of experience handling premium clients and a very accurate success and strategic ratio who always take decisions with observing each rish , security factors , cons and prons."},
                    {"role": "user" , "content": prompt}],
        )
        print(response.choices[0].message.content)
        






