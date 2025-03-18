# Implementing the Tool Pattern in Agentic AI

##### This Module implements working of Tools along with agents

**File:**  
📂 `ToolAgent/tool.py`

###### **Methods**
1. **`getFunction`**
    - Takes the function as an argument
    - Extracts out the funciton name , its description and parameters and returns in dictionary format.
    - Example of the output for the add function.

```json
{
    "name": "add",
    "description": "Adds two numbers.",
    "parameters": {
        "properties": {
            "x": {"type": "int"},
            "y": {"type": "int"}
        }
    }
}
```
2. **`ValidateArgumnets`**
  - Used for validating the arguments for a specific function
  - Takes `toolCall` as an input which contains the function arguments and checks them with the toolSignature which contains the expected types.
  - Rewrites the correct types if they do not match.

3. **`tool`**
- Takes a function, extracts its metadata using `getFunction` , wraps it inside an object using Tool class and return the Tool object

**Class Tool:** Wraps the function as an object
###### **Constructor**
- Stores the function name, function reference, and function metadata (fnSignature).
- Provides a run() method to execute the function with arguments.


**File:**  
📂 `ToolAgent/ToolAgent.py`

**BASE_GENERATION_SYSTEM_PROMPT**  is defined to give the context to llm about how you should behave while calling, about the arguments passed to you and how you should repsond to the queries.

**Class ToolAgent:** Represents a class which incorporates with the language model , use tools for assistance , valdiates arguments and responsible for running various tools.
###### **Constructor**
- Initializes the Groq AI client , sets the model , tool representing the list of available tools and maps the tool names with their corresponding Tool object and stores in `tools_dict`.

###### **Methods**
1. **`add_tool_signatures`**
 - Extracts out the tool signatures of all the avalaible tools and returns them in a concanated string format.

2. **`process_tool_calls`**
 - Processes each tool call, validates arguments, executes the tools, and collects results.
 - Finally , it returns the results in the dictionary format

3. **`run`**
- Use `buildPromptStructure` to format the user input , prepare the chat history using `ChatHistory` 
- Sends the structured request to the AI model (`completionCreate`).
- Extracts tool calls from the AI response using `extractTagContent()`.
- If tool calls exist:
    - Calls processToolCalls() to execute the functions.
     - Updates the chat history with tool results.
- Finally , returns the final response.