import json
from typing import Callable

def getFunction(fn : Callable) -> dict:
    fnSignature = {
        "name" : fn.__name__,
        "description" : fn.__doc__,
        "parameters" : {"properties" : {}},
    }
    schema = {
        k: {"type": v.__name__} for k, v in fn.__annotations__.items() if k != "return"
    }
    fnSignature["parameters"]["properties"] = schema
    return fnSignature 

def ValidateArgumnets(toolCall : dict , toolSignature : dict) ->dict :
    properties = toolSignature['parameters']['properties']

    type_mapping = {
        "int": int,
        "str": str,
        "bool": bool,
        "float": float,
    }
    for arg_name, arg_value in toolCall["arguments"].items():
        expected_type = properties[arg_name].get("type")

        if not isinstance(arg_value, type_mapping[expected_type]):
            toolCall["arguments"][arg_name] = type_mapping[expected_type](arg_value)

    return toolCall

class Tool:
    def __init__(self , name : str ,fn : Callable , fnSignature : str):
        self.name = name
        self.fn = fn
        self.fnSignature = fnSignature
    
    def __str__(self):
        return self.fnSignature
    def run(self , **kwargs):
        return self.fn(**kwargs)

def tool(fn : Callable):
    def wrapper():
        fnSignature = getFunction(fn)
        return Tool(
            name=fnSignature.get("name"), fn=fn, fnSignature =json.dumps(fnSignature)
        )
    return wrapper()


