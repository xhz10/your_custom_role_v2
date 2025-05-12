from chromadb import EmbeddingFunction, Documents, Embeddings
from crewai import Agent, Crew, Process, Task
from crewai.memory import LongTermMemory
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from crewai.project import CrewBase, agent, crew, task

from your_custom_role_v2.embedding.ZhiPuEmbedding import embedding
from your_custom_role_v2.listener.RoleListener import MyCustomListener

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


# role_listener = MyCustomListener()


class CustomEmbedder(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        # generate embeddings
        rsp = embedding(input)
        return rsp

@CrewBase
class YourCustomRoleV2():
    """YourCustomRoleV2 crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def dialogue_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['dialogue_generator'],
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def generate_dialogue_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_dialogue_task'],
        )


    @crew
    def crew(self) -> Crew:
        """Creates the YourCustomRoleV2 crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            memory=True,
            long_term_memory=LongTermMemory(
                storage=LTMSQLiteStorage(
                    db_path="./long_history/long_term_memory_storage.db"
                )
            ),
            embedder={
                "provider": "custom",
                "config": {
                    "embedder": CustomEmbedder()
                }
            }
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
