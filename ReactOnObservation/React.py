import json
import re
from dotenv import load_dotenv
import os
import requests
from  colorama import Fore
from groq import Groq

from confs.completions import ChatHistory
from confs.completions import completionCreate
from confs.completions import updateChatHistory
from confs.completions import buildPromptStructure
from confs.extraction import extractTagContent
from ToolAgent.tool import Tool
from ToolAgent.tool import ValidateArgumnets

load_dotenv()

