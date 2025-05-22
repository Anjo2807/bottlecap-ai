from openai import OpenAI
import discord
import dotenv
import os

dotenv.load_dotenv()
dc_token = os.getenv("DC_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

dc_client = discord.Client(intents=intents)

client = OpenAI(
  base_url="https://openrouter.ai/api/v1"
)

@dc_client.event
async def on_ready():
  print(f"logged in as {dc_client.user}")

@dc_client.event
async def on_message(message):
  if message.author == dc_client.user:
    return
  
  if message.content.startswith("bottlecap"):
    parts = message.content.split(" ")
    if len(parts) < 2:
            await message.reply("Please write a question or a response")
            return
    parts.pop(0)
    response = ' '.join(parts)
    print(response)
    try:
      completion = client.chat.completions.create(
        extra_body={},
        model="google/gemma-2-9b-it:free",
        messages=[
          {
            "role": "user",
            "content": response,
          }
        ]
      )
      await message.reply(completion.choices[0].message.content.strip())
    except Exception as e:
       print(e)
       await message.reply("Hey can you reprompt me? I have encountered a bug")
       return

dc_client.run(dc_token)

