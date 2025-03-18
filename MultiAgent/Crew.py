import json
import re
from textwrap import dedent
from collections import deque
from colorama import Fore
from graphviz import Digraph

from confs.logging import fancy_print


class Crew:
    currentCrew = None
    def __init__(self):
        self.agents = []
    
    def __enter__(self):
        Crew.currentCrew = self
        return self
    def __exit__(self,ExceptionType, ExceptionValue, ExecutionTraceback):
        Crew.currentCrew = None
    def addAgent(self, agent):
        self.agents.append(agent)

    @staticmethod
    def registerAgent(agent):
        if Crew.currentCrew is not None:
            Crew.currentCrew.addAgent(agent)
        else:
            raise Exception("No crew to register agent with")
    def topologicalSort(self):
        in_degree = {agent: len(agent.dependencies) for agent in self.agents}
        queue = deque([agent for agent in self.agents if in_degree[agent] == 0])

        sorted_agents = []

        while queue:
            current_agent = queue.popleft()
            sorted_agents.append(current_agent)

            for dependent in current_agent.dependents:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        if len(sorted_agents) != len(self.agents):
            raise ValueError(
                "Circular dependencies detected among agents, preventing a valid topological sort"
            )

        return sorted_agents
    
    def plot(self):
        dot = Digraph(format="png") 
        for agent in self.agents:
            dot.node(agent.name)
            for dependency in agent.dependencies:
                dot.edge(dependency.name, agent.name)
        return dot
    
    def run(self):
        sortedAgents = self.topologicalSort()
        for agent in sortedAgents:
            fancy_print(f"RUNNING AGENT: {agent}")
            print(Fore.RED + f"{agent.run()}")
