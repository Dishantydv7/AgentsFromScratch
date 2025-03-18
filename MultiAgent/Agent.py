import json 
import re 
from textwrap import dedent 

from confs.logging import fancy_print  
from ReactOnObservation.React import ReactAgent
from ToolAgent.tool import Tool
from MultiAgent.Crew import Crew


class Agent:
    def __init__(self , name : str , backstory : str , taskDescription : str ,taskExpectedOutput : str , tools : list[Tool] | None = None  , llm : str = "llama-3.3-70b-versatile"):
        self.name = name
        self.backstory = backstory
        self.taskDescription = taskDescription
        self.taskExpectedOutput = taskExpectedOutput
        self.react_agent = ReactAgent(model=llm, system_prompt=self.backstory, tools=tools or [])
        self.dependencies: list[Agent] = []
        self.dependents : list[Agent] = []
        self.context = ""
        Crew.registerAgent(self)

    def __repr__(self):
        return f"{self.name} : {self.backstory}"
    
    def __rshift__(self, other):
        self.addDependent(other)
        return other
    def __lshift__(self , other):
        self.addDependency(other)
        return other 
    def __rrshift__(self, other):
        self.addDependency(other)
        return self 
    def __rlshift__(self, other):
        self.addDependent(other)
        return self 
    def addDependent(self, other):
        if isinstance(other, Agent):
            other.dependencies.append(self)
            self.dependents.append(other)
        elif isinstance(other, list) and all(isinstance(item, Agent) for item in other):
            for item in other:
                item.dependencies.append(self)
                self.dependents.append(item)
        else:
            raise TypeError("The dependent must be an instance or list of Agent.")
    def addDependency(self, other):
        if isinstance(other, Agent):
            other.dependencies.append(self)
            self.dependents.append(other)
        elif isinstance(other, list) and all(isinstance(item, Agent) for item in other):
            for item in other:
                item.dependencies.append(self)
                self.dependents.append(item)
        else:
            raise TypeError("The dependent must be an instance or list of Agent.") 
        
    def recieveContext(self , inputData):
        self.context += f"{self.name} received context: \n{inputData}"

    def createPrompt(self):
        prompt = dedent(
            f"""
        You are an AI agent. You are part of a team of agents working together to complete a task.
        I'm going to give you the task description enclosed in <task_description></task_description> tags. I'll also give
        you the available context from the other agents in <context></context> tags. If the context
        is not available, the <context></context> tags will be empty. You'll also receive the task
        expected output enclosed in <task_expected_output></task_expected_output> tags. With all this information
        you need to create the best possible response, always respecting the format as describe in
        <task_expected_output></task_expected_output> tags. If expected output is not available, just create
        a meaningful response to complete the task.

        <task_description>
        {self.taskDescription}
        </task_description>

        <task_expected_output>
        {self.taskExpectedOutput}
        </task_expected_output>

        <context>
        {self.context}
        </context>

        Your response:
        """
        ).strip()

        return prompt
    
    def run(self):
        msg = self.createPrompt()
        output = self.react_agent.run(user_msg=msg)

        for dependent in self.dependents:
            dependent.recieveContext(output)
        return output
    





        
