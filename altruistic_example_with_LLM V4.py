!pip install -q -U google-generativeai
!pip install protobuf==3.20.*
!pip show google-generativeai

import google.generativeai as genai
import time

# API key and LLM setup
GOOGLE_API_KEY = 'AIzaSyA2H75MOyP5EcDRSeaPFj8u1XBUrTkpdDI'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-002')

# Agent A's current energy and energy needed for the upcoming process
agent_A_current_energy = 30  # kW
agent_A_energy_needed = 35  # kW (Energy needed for the upcoming process)

# Agent B's current energy and energy needed for the upcoming process
agent_B_current_energy = 25  # kW
agent_B_energy_needed = 10  # kW (Energy needed for the upcoming process)

# Agent A sends a request
def agent_A_request(requested_energy):
    return f"Please share {requested_energy} kW of energy."

# Agent B evaluates the request
def agent_B_response(request, agent_B_current_energy, agent_B_energy_needed, requested_energy):
    prompt = f"""
    You have {agent_B_current_energy} kW of energy available, and you need {agent_B_energy_needed} kW for your upcoming process.
    You received a request: "{request}" for {requested_energy} kW of energy.
    Decide whether to AGREE or REFUSE the request:
    - If the requested energy exceeds your available energy, REFUSE.
    - If sharing the requested energy leaves you with enough for your upcoming process, AGREE.
    - Otherwise, REFUSE.
    Respond briefly: AGREE or REFUSE, followed by reasoning.
    """
    return model.generate_content(prompt).text.strip()

# Main interaction
if __name__ == "__main__":
    # Check if Agent A has enough energy before making a request
    if agent_A_current_energy >= agent_A_energy_needed:
        print(f"Agent A: I have enough energy ({agent_A_current_energy} kW) for my upcoming process.")
    else:
        requested_energy = agent_A_energy_needed - agent_A_current_energy  # Energy required from Agent B
        request = agent_A_request(requested_energy)
        print(f"Agent A: {request}")

        # Record the start time
        start_time = time.time()

        response = agent_B_response(request, agent_B_current_energy, agent_B_energy_needed, requested_energy)

        # Record the end time
        end_time = time.time()

        # Calculate the time taken to generate the response
        time_taken = end_time - start_time
        print(f"Agent B: {response}")
        print(f"Time taken for the response: {time_taken:.4f} seconds")

        # If Agent B agrees to share energy, update the energy values for both agents
        if 'AGREE' in response:
            agent_A_current_energy += requested_energy  # Agent A receives energy
            agent_B_current_energy -= requested_energy  # Agent B shares energy
            print(f"\nEnergy successfully shared!")
            print(f"Agent A's new energy: {agent_A_current_energy} kW")
            print(f"Agent B's new energy: {agent_B_current_energy} kW")
        else:
            print("\nAgent B refused to share the requested energy.")
