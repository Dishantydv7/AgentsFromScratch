# Implementing the Reflection Pattern in Agentic AI

##### This Module implements Reflection Pattern of Agentic AI (Evaluator-optimizer in Anthropic Docs)

**BASE_GENERATION_SYSTEM_PROMPT** is defined to use as a system prompt for generation calls.
**BASE_UPDATE_SYSTEM_PROMPT** is defined to use as a system prompt for evaluator calls.

![Reflection Pattern](../Images/SelfLoop.png?raw=true "Reflection Pattern")


**Class Reflection:**
###### **Constructor**
- Initializes a client instance and sets the AI model to be used for processing.

###### **Methods**
1. **`_requestCompletion`**
     - Sends the request to the corresponding model.
     - Takes `history`, `verbose`, `log_title`, and `log_color` as parameters.
     - Calls the model for response and returns the response.
2. **`generate`**
     - Calls the method(`_requestCompletion`) to get the response for the generator subsection with keeping the context of generation_history
3. **`reflect`**
    - Calls the method (`_requestCompletion`) to get the response for the reflector or evaluator subsection with keeping the context of reflection_history
4. **`run`**
     - It takes the user message and iterates over the generation-reflection cycle until a stopping condition is met or the maximum number of steps is exhausted.
     - In each iteration :
    1.  The generate method is called ,the generated content is appended to   generation_history and reflection history based on the sub section.
    2.  Finally, if the critique is <OK> then the loop is stopped 
    3. After the loop , the final generated content is returned 

**Implementation File:**  
📂 `SelfLoopClass/ReflectionPattern/SelfLoop.ipynb`

Ref :
https://www.anthropic.com/engineering/building-effective-agents