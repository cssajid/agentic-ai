from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field
from typing import List
from .tools.push_tool import PushNotificationTool
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage

class TrendingCompany(BaseModel):
    """A company that is in the news and attracting attention"""
    name:str=Field(description="The name of the company")
    ticker:str=Field(description="Stock ticker symbol for the company")
    reason:str=Field(description="Reason why the company is trending")

class TrendingCompanyList(BaseModel):
    """List of multiple trending companyies taht are in news and attracting attention"""
    companies:List[TrendingCompany]=Field(description="List of trending companies")

class TrendingCompanyResearch(BaseModel):
    """Detailed research on a trending company"""
    name:str=Field(description="The name of the company")
    market_position:str=Field(description="The current market position of the company and competitive analysis")
    futue_outlook:str=Field(description="Investment potential and suitability for different types of investors")

class TrendingCompanyResearchList(BaseModel):
    """A list of detailed research of all trending companies"""
    research_list:List[TrendingCompanyResearch]=Field(description="Comprehensive research on all trending companies")


@CrewBase
class StockPicker():
    """StockPicker crew"""

    agents_config:'config/agenmts.yaml' 
    tasks_config: 'config/tasks.yaml'

    @agent
    def trending_company_finder(self) -> Agent:
        return Agent(config=self.agents_config['trending_company_finder'],tools=[SerperDevTool()],memory=True) 
    
    @agent
    def financial_researcher(self) -> Agent:
        return Agent(config=self.agents_config['financial_researcher'],tools=[SerperDevTool()]) 

    @agent
    def stock_picker(self) -> Agent:
        return Agent(config=self.agents_config['stock_picker'],tools=[PushNotificationTool()],memory=True)

    @task
    def find_trending_companies(self) -> Task:
        return Task(config=self.tasks_config['find_trending_companies'],output_pydantic=TrendingCompanyList)
    
    @task
    def research_trending_companies(self) -> Task:
        return Task(config=self.tasks_config['research_trending_companies'],output_pydantic=TrendingCompanyResearchList)
    
    @task
    def pick_best_company(self) -> Task:
        return Task(config=self.tasks_config['pick_best_company'])

    @crew
    def crew(self) -> Crew:
        """Create stock picker crew and run the process to find the best stock to invest in"""
        
        manager=Agent(
            config=self.agents_config['manager'],
            allow_delegate=True
        )

        return Crew(
            agents=self.agents,
            tasks=self.tasks, 
            process=Process.hierarchical,
            verbose=True,
            manager_agent=manager,
            memory=True,
            long_term_memory = LongTermMemory(
                storage=LTMSQLiteStorage(
                    db_path="./memory/long_term_memory_storage.db"
                )
            ),
            short_term_memory = ShortTermMemory(
                storage = RAGStorage(
                        embedder_config={
                            "provider": "openai",
                            "config": {
                                "model": 'text-embedding-3-small'
                            }
                        },
                        type="short_term",
                        path="./memory/"
                    )
                ),
            entity_memory = EntityMemory(
                storage=RAGStorage(
                    embedder_config={
                        "provider": "openai",
                        "config": {
                            "model": 'text-embedding-3-small'
                        }
                    },
                    type="short_term",
                    path="./memory/"
                )
            ),
        )
