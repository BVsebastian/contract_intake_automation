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

def process_contracts():
    """
    Process all contract PDFs in the contracts directory.
    """
    # Get path to contracts directory
    contracts_dir = Path(__file__).parent / 'contracts'
    
    if not contracts_dir.exists():
        print(f"Error: Contracts directory not found: {contracts_dir}")
        sys.exit(1)

    # Get all PDF files in the contracts directory
    contract_files = list(contracts_dir.glob('*.pdf'))
    
    if not contract_files:
        print(f"Error: No PDF files found in {contracts_dir}")
        sys.exit(1)

    print(f"\nFound {len(contract_files)} contract(s) to process")
    print("=" * 50)

    # Process each contract
    successful = []
    failed = []

    for contract_path in contract_files:
        try:
            # Get contract name without .pdf extension
            contract_name = contract_path.stem
            
            print(f"\nProcessing: {contract_path.name}")
            print(f"Output folder: output/{contract_name}/")
            print("-" * 30)

            # Create inputs for the crew
            inputs = {
                'contract_path': str(contract_path),
                'contract_name': contract_name
            }
            
            # Process the contract
            ContractIntakeAgents().crew().kickoff(inputs=inputs)
            
            successful.append(contract_path.name)
            print(f"✔ Successfully processed: {contract_path.name}")
            print(f"✔ Output saved to: output/{contract_name}/")
            
        except Exception as e:
            failed.append((contract_path.name, str(e)))
            print(f"❌ Error processing {contract_path.name}: {e}")
            continue

    # Print summary
    print("\n" + "=" * 50)
    print("Processing Summary:")
    print(f"Total contracts: {len(contract_files)}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")

    if successful:
        print("\nSuccessfully processed:")
        for contract in successful:
            print(f"✔ {contract}")

    if failed:
        print("\nFailed to process:")
        for contract, error in failed:
            print(f"❌ {contract} - {error}")

if __name__ == "__main__":
    process_contracts()

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
