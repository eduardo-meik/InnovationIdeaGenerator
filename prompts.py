# Define prompts for each user input field
PROBLEM_STATEMENT_PROMPT = {
    'prompt': "Improve the following problem statement in spanish: ",
    'max_tokens': 100  # example length; adjust as needed
}

NEED_FOR_INNOVATION_PROMPT = {
    'prompt': "Refine the justification for this innovation in spanish: ",
    'max_tokens': 100
}

INNOVATION_NAME_PROMPT = {
    'prompt': "Provide a succinct name for the following innovation idea in spanish: ",
    'max_tokens': 15
}

INNOVATION_DESCRIPTION_PROMPT = {
    'prompt': "Summarize the description of this innovation in spanish: ",
    'max_tokens': 150
}

EXPECTATIONS_PROMPT = {
    'prompt': "Clarify the following expectations from creator to ask to the company regarding the idea, in spanish: ",
    'max_tokens': 75
}

FINAL_REPORT_PROMPT = {
    'prompt': "Compile and generate a concise market research report based on the following details in spanish with references: ",
    'max_tokens': 500  # This can be adjusted as per requirement
}

GLOBAL_TEMPERATURE = 0.8  # Adjust this as needed for desired randomness in results

