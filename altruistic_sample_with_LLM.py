#First install these libraries

!pip install -q -U google-generativeai
!pip install protobuf==3.20.*
!pip show google-generativeai

##Imports
import google.generativeai as genai

# API key and LLM setup
GOOGLE_API_KEY = google_api_key
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-002')

# Agent B's available energy
agent_B_energy = 25  # kW

# Agent A sends a request
def agent_A_request(requested_energy):
    return f"Please share {requested_energy} kW of energy."

# Agent B evaluates the request
def agent_B_response(request, available_energy):
    prompt = f"""
    You have {available_energy} kW of energy available. 
    Decide whether to AGREE or REFUSE the request: "{request}". 
    If the request exceeds your available energy, REFUSE. Otherwise, AGREE.
    Respond briefly: AGREE or REFUSE, followed by reasoning.
    """
    return model.generate_content(prompt).text.strip()

# Main interaction
if __name__ == "__main__":
    requested_energy = 20  # kW
    request = agent_A_request(requested_energy)
    print(f"Agent A: {request}")

    response = agent_B_response(request, agent_B_energy)
    print(f"Agent B: {response}")
