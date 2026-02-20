import sys
import pathlib

# make src importable
sys.path.append(str(pathlib.Path(__file__).resolve().parent / "src"))

from agent.agent_core import create_agent

print("Creating agent...")
agent = create_agent()
print("Agent created. Running demo (fetch + extract)...")

# Simple instruction: agent should call tools fetch_webpage and extract_selectors
instruction = (
    "Fetch the webpage at https://example.com and extract the text for the CSS selector 'h1'. "
    "Return only the extracted text in plain form."
)

try:
    inputs = {"messages": [{"role": "user", "content": instruction}]}

    # Try supported execution methods for the compiled agent graph.
    if hasattr(agent, "stream"):
        print("Using agent.stream()...")
        out = ""
        for chunk in agent.stream(inputs, stream_mode="updates"):
            print(chunk)
            out = chunk
        print("Final output:\n", out)
    elif callable(agent):
        print("Calling agent(...) directly...")
        resp = agent(inputs)
        print(resp)
    elif hasattr(agent, "run"):
        print("Using agent.run()...")
        resp = agent.run(inputs)
        print(resp)
    else:
        print("No known execution method found on agent object.\n", dir(agent))
except Exception as e:
    print("Agent run failed:", e)
    raise
