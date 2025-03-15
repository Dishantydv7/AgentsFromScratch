import re
from dataclasses import dataclass

@dataclass
class TagContentResult:
    content : list[str]
    found : bool

def extractTagContent(text : str ,tag :str) -> TagContentResult:
    tagPattern = rf"<{tag}>(.*?)</{tag}>"
    matchedContents  = re.findall(tagPattern, text, re.DOTALL)
    return TagContentResult(
        content=[content.strip() for content in matchedContents],
        found=bool(matchedContents),
    )
