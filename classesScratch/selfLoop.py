from colorama import Fore
from dotenv import load_dotenv
import os 
from groq import Groq

from confs.completions import buildPromptStructure
from confs.completions import completionCreate
from confs.completions import updateChatHistory
from confs.completions import FixedFirstChatHistory
from confs.logging import fancy_step_tracker

load_dotenv()

BASE_GENERATION_SYSTEM_PROMPT = """
Your task is to Generate the best content possible for the user's request.
If the user provides critique, respond with a revised version of your previous attempt.
You must always output the revised content.
"""

BASE_UPDATE_SYSTEM_PROMPT = """
You are tasked with generating critique and recommendations to the user's generated content.
If the user content has something wrong or something to be improved, output a list of recommendations
and critiques. If the user content is ok and there's nothing to change, output this: <OK>
"""

class ReflectionAgent:
    def __init__(self , model : str = "llama-3.3-70b-versatile" ):
        self.client = Groq()
        self.model = model

    def _requestCompletion(self ,history : list , verbose : int = 0 , log_title : str = "COMPLETION" , log_color :str = "" ):
        response = completionCreate(self.client , history , self.model)

        if verbose>0 :
            print(log_color, f"\n\n{log_title}\n\n", response)
        
        return response

    def generate(self, generation_history: list, verbose: int = 0) -> str:
        return self._requestCompletion(
            generation_history, verbose, log_title="GENERATION", log_color=Fore.BLUE
        )
    
    def reflect(self, reflection_history: list, verbose: int = 0) -> str:
        return self._requestCompletion(
            reflection_history, verbose, log_title="REFLECTION", log_color=Fore.GREEN
        )
    
    def run(self , userMsg : str , verbose : int = 0 , nSteps : int =10 , generation_system_prompt : str = "" , reflection_system_prompt : str = ""):
        generation_system_prompt += BASE_GENERATION_SYSTEM_PROMPT
        reflection_system_prompt += BASE_UPDATE_SYSTEM_PROMPT

        generation_history = FixedFirstChatHistory(
            [
                buildPromptStructure(prompt=generation_system_prompt, role="system"),
                buildPromptStructure(prompt=userMsg, role="user"),
            ],
            total_length=3,
        )

        reflection_history = FixedFirstChatHistory(
            [buildPromptStructure(prompt=reflection_system_prompt, role="system")],
            total_length=3,
        )

        for step in range(nSteps):
            if verbose > 0:
                fancy_step_tracker(step, nSteps)

            generation = self.generate(generation_history, verbose=verbose)
            updateChatHistory(generation_history, generation, "assistant")
            updateChatHistory(reflection_history, generation, "user")

            critique = self.reflect(reflection_history, verbose=verbose)

            if "<OK>" in critique:
                print(
                    Fore.RED,
                    "\n\nStop Sequence found. Stopping the reflection loop ... \n\n",
                )
                break

            updateChatHistory(generation_history, critique, "user")
            updateChatHistory(reflection_history, critique, "assistant")

        return generation
    


    
