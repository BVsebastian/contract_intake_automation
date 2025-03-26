from setuptools import setup, find_packages

setup(
    name="contract_intake_agents",
    version="0.1.0",
    packages=find_packages(where="contract_intake_agents/src"),
    package_dir={"": "contract_intake_agents/src"},
    install_requires=[
        "crewai",
        "crewai_tools",
    ],
) 