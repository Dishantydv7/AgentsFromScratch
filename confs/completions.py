def completionCreate(client , messages : list , model : str)-> str:
    response = client.chat.completions.create(
        messages = messages,
        model = model
    )
    return str(response.choices[0].message.content)

def buildPromptStructure(prompt : str , role : str ,tag : str = "")->dict:
    if tag:
        prompt = f"<{tag}>{prompt}</{tag}>"
    return {"role": role, "content": prompt}

def updateChatHistory(history : list , msg : str , role : str)->list:
    history.append(buildPromptStructure(prompt=msg , role=role))

class ChatHistory(list):
    def __init__(self , messages : list | None  = None, totalLength : int = -1):
        if messages is None:
            messages = []

        super().__init__(messages)
        self.totalLength = totalLength

    def append(self ,message:str):
        if(len(self) == self.totalLength):
            self.pop(0)
        super().append(message)


class FixedFirstChatHistory(ChatHistory):
    def __init__(self, messages: list | None = None, total_length: int = -1):
        super().__init__(messages)
        self.total_length = total_length

    def append(self, msg: str):
        if len(self) == self.total_length:
            self.pop(1)
        super().append(msg)



