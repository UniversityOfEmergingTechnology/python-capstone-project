from openai import OpenAI
from config import apikey
client = OpenAI(api_key = apikey)


response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {
      "role": "user",
      "content": "Give me a resignation letter"
    }
  ],
  temperature=1,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

# Accessing the message content
if response.choices:
    message_content = response.choices[0].message.content
    print(message_content)
else:
    print("No response generated.")