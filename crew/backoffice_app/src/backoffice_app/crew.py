from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel, Field


class FinalRecommendation(BaseModel):
    """
    Final decision returned by the Decision Agent
    """

    action_taken: str = Field(
        description=(
            "Final action selected by the decision agent. "
            "Must match one of the available actions provided in input "
            "such as approved, reject, or more_info."
        )
    )

    analysis: str = Field(
        description=(
            "Detailed explanation describing why the decision was taken, "
            "including document validation results, comparison findings, "
            "business rule evaluation, and any detected issues."
        )
    )

    confidence_score: int = Field(
        description=(
            "Numeric confidence score between 0 and 100 representing "
            "the reliability of the final decision."
        ),
        ge=0,
        le=100
    )

@CrewBase
class BackofficeApp():
    """BackofficeApp crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def document_validator(self) -> Agent:
        return Agent(
            config=self.agents_config['document_validator'],
            verbose=True,
        )
    
    @agent
    def comparison_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['comparison_agent'],
            verbose=True,
        )
    
    @agent
    def business_rules_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['business_rules_agent'],
            verbose=True,
        )

    @agent
    def decision_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['decision_agent'],
            verbose=True,
        )

    @task
    def document_validation_task(self) -> Task:
        return Task(
            config=self.tasks_config['document_validation_task']
        )
    
    @task
    def comparison_task(self) -> Task:
        return Task(
            config=self.tasks_config['comparison_task']
        )
    
    @task
    def business_rules_task(self) -> Task:
        return Task(
            config=self.tasks_config['business_rules_task']
        )

    @task
    def decision_task(self) -> Task:
        return Task(
            config=self.tasks_config['decision_task'],
            output_pydantic=FinalRecommendation
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )