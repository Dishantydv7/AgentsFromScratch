This project is implementing a relfective architecture of ai agent systems that iteratively enhances generated responses through self-reflection. It employs a language model to generate content, critiques its own output, and refines responses until an optimal version is produced. The system is designed for applications that require high-quality content generation and iterative improvement.

## Features

- **Iterative Content Refinement**: Uses self-feedback to enhance responses.
- **Dynamic Chat History Management**: Tracks and updates interactions efficiently.
- **Structured Prompting**: Implements tagged prompts for better AI understanding.
- **Flexible Model Integration**: Currently supports `llama-3.3-70b-versatile`, but can be adapted for other models.
- **Logging and Debugging Utilities**: Provides colorful logs for better tracking.

## File Structure

- `completions.py`: Handles chat completion requests, chat history management, and message structuring.
- `selfLoop.py`: Implements the `ReflectionAgent`, which orchestrates content generation and refinement.
- `extraction.py`: Provides functions for extracting tagged content from generated text.
- `logging.py`: Contains logging utilities for tracking execution steps.

## Installation
```sh
pip install -r requirements.txt
