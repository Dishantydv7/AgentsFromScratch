import json
import re
from  colorama import Fore 
from typing import Callable
from dotenv import load_dotenv
from groq import Groq

from ToolAgent.tool import Tool
from ToolAgent.tool import ValidateArgumnets
from confs.completions import buildPromptStructure
from confs.completions import ChatHistory
from confs.completions import completionCreate
from confs.completions import updateChatHistory
from confs.extraction import extractTagContent

load_dotenv()

TOOL_SYSTEM_PROMPT = """
You are a function calling AI model. You are provided with function signatures within <tools></tools> XML tags.
You may call one or more functions to assist with the user query. Don't make assumptions about what values to plug
into functions. Pay special attention to the properties 'types'. You should use those types as in a Python dict.
For each function call return a json object with function name and arguments within <tool_call></tool_call>
XML tags as follows:

<tool_call>
{"name": <function-name>,"arguments": <args-dict>,  "id": <monotonically-increasing-id>}
</tool_call>

Here are the available tools:

<tools>
%s
</tools>
"""

class ToolAgent:
    def __init__(self, tools : Tool , model: str = "llama-3.3-70b-versatile") -> None:
        self.client = Groq()
        self.model = model
        self.tools = tools if isinstance(tools, list) else [tools]
        self.tools_dict = {tool.name: tool for tool in self.tools}

    def addToolSignature(self) -> str:
        return "".join([tool.fnSignature for tool in self.tools])
    
    def processToolCalls(self , tool_calls_content : str) -> dict:
        # keys are tool call IDs and values are the results from the tools.
        
        observation = {}
        for tool_call_str in tool_calls_content:
            toolCall = json.loads(tool_call_str)
            tool_name = toolCall["name"]
            tool = self.tools_dict[tool_name]

            print(Fore.GREEN + f"\nUsing Tool: {tool_name}")

            validateToolCall = ValidateArgumnets(toolCall , json.loads(tool.fnSignature))
            print(Fore.GREEN + f"\nTool call dict: \n{validateToolCall}")

            result = tool.run(**validateToolCall["arguments"])
            print(Fore.GREEN + f"\nTool result: \n{result}")

            observation[validateToolCall["id"]] = result

        return observation
    
    def run(self , msg : str , ) -> str:
        userPrompt = buildPromptStructure(prompt=msg , role="user")
        toolChatHistory = ChatHistory([
            buildPromptStructure(prompt=TOOL_SYSTEM_PROMPT %  self.addToolSignature() , role="system"),
            userPrompt
        ]) 
        agentChatHistory = ChatHistory([userPrompt])
        toolCallResponse = completionCreate(self.client , toolChatHistory , self.model)
        toolCalls = extractTagContent(str(toolCallResponse), "toolCall")

        if toolCalls.found:
            observations = self.processToolCalls(toolCalls.content)
            updateChatHistory(
                agentChatHistory, f'f"Observation: {observations}"', "user"
            )

        return completionCreate(self.client, agentChatHistory, self.model)

            

