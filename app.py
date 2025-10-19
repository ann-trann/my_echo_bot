import asyncio
from aiohttp import web
from botbuilder.core import (
    BotFrameworkAdapter,
    BotFrameworkAdapterSettings,
    TurnContext,
)
from botbuilder.schema import Activity
import json

# ---- Load data from file ----
with open("data.json", "r", encoding="utf-8") as f:
    knowledge_base = json.load(f)

# ---- Adapter setup ----
SETTINGS = BotFrameworkAdapterSettings("", "")
ADAPTER = BotFrameworkAdapter(SETTINGS)

# ---- Handle messages ----
async def handle_messages(req: web.Request):
    body = await req.json()
    activity = Activity().deserialize(body)

    async def logic(turn_context: TurnContext):
        user_input = (turn_context.activity.text or "").lower().strip()

        # Match input with keys in data.json
        response = None
        for key, value in knowledge_base.items():
            if key in user_input:
                response = value
                break

        if not response:
            response = "Sorry, I don’t have information about that yet."

        await turn_context.send_activity(response)

    await ADAPTER.process_activity(activity, "", logic)
    return web.Response(status=200)

# ---- App setup ----
APP = web.Application()
APP.router.add_post("/api/messages", handle_messages)

if __name__ == "__main__":
    print("Bot is running on http://localhost:3978/api/messages")
    web.run_app(APP, host="localhost", port=3978)
