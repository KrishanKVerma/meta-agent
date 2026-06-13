import os
from dotenv import load_dotenv
from groq import Groq
import json

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def calculate(expression):
    return eval(expression)

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a math expression and return the result",
            "parameters":{
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The math expression , e.g. '3+4' or '322/2' "
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

prompt = input("Ask me something related to calculation: ")
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": prompt}],
    tools=tools
)

tool_call = response.choices[0].message.tool_calls[0]

print(response.choices[0].message)

args = json.loads(tool_call.function.arguments)
expression = args["expression"]
answer = calculate(expression)
print("Answer:", answer)