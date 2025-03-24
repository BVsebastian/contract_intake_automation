import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
from pathlib import Path
from crewai_tools import PDFSearchTool, FileWriterTool
import sys
from tools.excel_writer_tool import ExcelWriterTool

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

load_dotenv()   

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class ContractIntakeAgents():
    """ContractIntakeAgents crew for automated contract processing"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    output_dir = Path(__file__).parent / 'output'  # Class variable

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools

    def __init__(self):
        pass  # Remove directory creation from here

    @classmethod
    def ensure_output_dir(cls):
        cls.output_dir.mkdir(exist_ok=True)

    @agent
    def contract_analyst(self) -> Agent:
        pdf_tool = PDFSearchTool()
        file_writer_tool = FileWriterTool()
        excel_writer_tool = ExcelWriterTool()
        
        return Agent(
            config=self.agents_config['contract_analyst'],
            tools=[pdf_tool, file_writer_tool, excel_writer_tool],
            verbose=True
        )

    @agent
    def contract_validator(self) -> Agent:
        return Agent(
            config=self.agents_config['contract_validator'],
            verbose=True
        )

    @agent
    def notification_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['notification_specialist'],
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def contract_analyst_task(self) -> Task:
        return Task(
            config=self.tasks_config['contract_analyst_task'],
            output_files=[
                'output/{contract_name}_extracted_contract_details.json',
                'output/{contract_name}_extracted_contract_details.csv',
                'output/{contract_name}_extracted_contract_details.xlsx'
            ]
        )

    @task
    def contract_validator_task(self) -> Task:
        return Task(
            config=self.tasks_config['contract_validator_task'],
            output_file='output/{contract_name}_validated_contract_data.json'
        )

    @task
    def notification_specialist_task(self) -> Task:
        return Task(
            config=self.tasks_config['notification_specialist_task'],
            output_file='output/{contract_name}_email_summary.txt'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ContractIntakeAgents crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )