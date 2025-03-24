#!/usr/bin/env python
import sys
import warnings
from pathlib import Path
from datetime import datetime

from crew import ContractIntakeAgents

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew with contract processing inputs.
    """
    if len(sys.argv) < 3:
        print("Usage: python main.py <contract_path> <contract_name>")
        sys.exit(1)

    contract_path = sys.argv[1]
    contract_name = sys.argv[2]

    # Validate contract file exists and is PDF
    path = Path(contract_path)
    if not path.exists():
        print(f"Error: Contract file not found: {contract_path}")
        sys.exit(1)
    if path.suffix.lower() != '.pdf':
        print(f"Error: Contract file must be a PDF: {contract_path}")
        sys.exit(1)
    
    inputs = {
        'contract_path': str(path),
        'contract_name': contract_name
    }
    
    try:
        ContractIntakeAgents().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

if __name__ == "__main__":
    run()

# def train():
#     """
#     Train the crew for a given number of iterations.
#     """
#     inputs = {
#         "topic": "AI LLMs"
#     }
#     try:
#         ContractIntakeAgents().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while training the crew: {e}")

# def replay():
#     """
#     Replay the crew execution from a specific task.
#     """
#     try:
#         ContractIntakeAgents().crew().replay(task_id=sys.argv[1])

#     except Exception as e:
#         raise Exception(f"An error occurred while replaying the crew: {e}")

# def test():
#     """
#     Test the crew execution and returns the results.
#     """
#     inputs = {
#         "topic": "AI LLMs",
#         "current_year": str(datetime.now().year)
#     }
#     try:
#         ContractIntakeAgents().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while testing the crew: {e}")
