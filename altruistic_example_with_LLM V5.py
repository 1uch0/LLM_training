!pip install -q -U google-generativeai
!pip install protobuf==3.20.*
!pip show google-generativeai

import google.generativeai as genai
import time

# API key and LLM setup
GOOGLE_API_KEY = google_api_key #Write the API KEY here
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-002')

# Agent A and Agent B tool status (tool type: pick and place)
agent_A_tools = [{'tool_id': 1, 'tool_type': 'pick and place', 'wear_level': 30}]  # Tool with 30% wear
agent_B_tools = [{'tool_id': 2, 'tool_type': 'pick and place', 'wear_level': 60}]  # Tool with 60% wear

# Number of tools needed for the upcoming process
agent_B_tools_needed = 1  # Agent B needs 1 tool

# Function for Agent A to send a request for a tool
def agent_A_request(requested_tools, requested_tool_type):
    return f"Agent B, I need {requested_tools} tool(s) of type {requested_tool_type}."

# Function to generate the prompt based on the agent's tool status
def generate_prompt(agent_A_tools, agent_B_tools, agent_B_tools_needed):
    agent_A_tool = agent_A_tools[0]
    agent_B_tool = agent_B_tools[0]
    
    return f"""
    Agent A has a tool with wear level {agent_A_tool['wear_level']}%. 
    Agent B has a tool with wear level {agent_B_tool['wear_level']}%. 
    Agent B needs {agent_B_tools_needed} tool(s) of type pick and place.
    Should Agent B share their tool with Agent A? If so, what reasoning should be considered (tool wear, availability, etc.)?
    """

# Agent B evaluates the request
def agent_B_response(request, agent_A_tools, agent_B_tools, agent_B_tools_needed):
    prompt = generate_prompt(agent_A_tools, agent_B_tools, agent_B_tools_needed)
    
    start_time = time.time()
    response = model.generate_content(prompt).text.strip()
    end_time = time.time()
    
    time_taken = end_time - start_time
    
    return response, time_taken

# Main interaction
if __name__ == "__main__":
    requested_tools = agent_B_tools_needed  # Tools required by Agent B
    request = agent_A_request(requested_tools, 'pick and place')
    print(f"Agent A: {request}")
    
    # Evaluate the tool sharing decision
    response, time_taken = agent_B_response(request, agent_A_tools, agent_B_tools, requested_tools)
    print(f"Agent B: {response}")
    print(f"Time Taken: {time_taken:.4f} seconds")
    
    # Update tools if sharing occurs
    if 'AGREE' in response:
        print("Agent B agrees to share the tool. Updating tool statuses.")
        agent_B_tools[0]['wear_level'] += 10  # Assuming wear level increases after sharing
        print(f"New wear level of Agent B's tool: {agent_B_tools[0]['wear_level']}%")
