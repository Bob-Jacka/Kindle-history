import aiohttp
import requests
from langchain.agents import (
    AgentExecutor,
    create_openai_tools_agent
)
from langchain.callbacks.base import BaseCallbackHandler
from langchain.tools import tool
from langchain_openai import ChatOpenAI

system_prompt = """
Ты — агент, который решает задачи с помощью инструментов.
Перед каждым вызовом инструмента объясняй свой план в 1–2 предложениях.
Не раскрывай внутренние скрытые рассуждения, но давай понятные пользователю объяснения.
"""


# TODO change into english language

class JsonLogger(BaseCallbackHandler):
    def on_tool_start(self, tool, input, **kwargs):
        log = {
            "event": "tool_start",
            "tool": tool.name,
            "input": input,
        }
        print(json.dumps(log, ensure_ascii=False))

    def on_tool_end(self, output, **kwargs):
        log = {
            "event": "tool_end",
            "output": output,
        }
        print(json.dumps(log, ensure_ascii=False))

    def on_llm_start(self, serialized, prompts, **kwargs):
        log = {
            "event": "llm_start",
            "prompts": prompts,
        }
        print(json.dumps(log, ensure_ascii=False))

    def on_llm_end(self, response, **kwargs):
        log = {
            "event": "llm_end",
            "response": response,
        }
        print(json.dumps(log, ensure_ascii=False))


class DebugLogger(BaseCallbackHandler):
    def on_tool_start(self, tool, input, **kwargs):
        print(f"[TOOL START] {tool.name}({input})")

    def on_tool_end(self, output, **kwargs):
        print(f"[TOOL END] result={output}")

    def on_llm_start(self, serialized, prompts, **kwargs):
        print("[LLM START]")
        for p in prompts:
            print("Prompt:", p)

    def on_llm_end(self, response, **kwargs):
        print("[LLM END]")
        print("Response:", response)


class Agent:
    llm = ChatOpenAI(model="gpt-4o-mini", messages=[('system', system_prompt)])

    def __init__(self):
        self.agent = create_openai_tools_agent(
            llm=llm,
            tools=[multiply],  # TODO change tools
        )
        self.executor = AgentExecutor(agent=agent, tools=[multiply], callbacks=[DebugLogger()], )

    @tool
    async def async_weather(self, city: str) -> str:
        """
        Async weather report; You may think, why book manager provides async weather getter, if you have this question, please close this code
        """

        async with aiohttp.ClientSession() as session:
            geo_url = "https://api.api-ninjas.com/v1/geocoding"
            geo_params = {"city": city}
            async with session.get(geo_url, params=geo_params) as geo_resp:
                geo_data = await geo_resp.json()
                lat = geo_data[0]["latitude"]
                lon = geo_data[0]["longitude"]

            weather_url = "https://api.open-meteo.com/v1/forecast"
            weather_params = {"latitude": lat, "longitude": lon, "current_weather": True}
            async with session.get(weather_url, params=weather_params) as w_resp:
                weather_data = await w_resp.json()
                return weather_data["current_weather"]
