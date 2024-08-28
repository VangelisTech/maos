from enum import Enum
from typing import List, Optional
import daft
from pydantic import Field
from ray import serve
from ray.serve.handle import DeploymentHandle, DeploymentResponse

from src.core.tools.tool import Tool
from src.core.models.language.base import LLM
from src.core.data.domain.base.domain_object import DomainObject

class AgentStatus(str, Enum):
    IDLE = "idle"
    PENDING = "pending"
    WAITING = "waiting"
    PROCESSING = "processing"


@serve.deployment
class Agent(DomainObject):
    """
    The base agent class.
    """
    def __init__(self):
        name: Optional[str] = Field(
            default_factory=f"Agent {self.id}",
            description="The name of the agent", 
        ),
        status: AgentStatus = Field(
            default="Idle",
            description="The status of the agent"
        ),
        llm: Optional[LLM] = Field(
            default= MMLLM(),
            description="The Multimodal Model"
        ),
        reasoning: Optional[DeploymentHandle] = Field(
            default=MultiModalLLM(),
            description="The embedding model"
        ),
        memory: Optional[DeploymentHandle] = Field(
            ...,
            description="The embedding model",
        ),
        embedding: Optional[DeploymentHandle] = Field(
            default=MultiModalEmbedding(),
            description="The embedding model"
        ),
        tools: Optional[List[BaseTool]] = Field(
            default=None,
            description="The tools that the agent can use"
        ),
    ):
        super().__init__(metadata=)
        self.name =  name
        self.models = models
        self.reasoning = reasoning
        self.embedding = embedding
        self.tools = tools
        self.memory = 

        self.settings.MAX_NUM_PENDING_TASKS = 100
        self.settings.MAX_CONCURRENT_TASKS = 10


def __call__(self, request: Request, task: Task):
    prompt = Request.Prompt
    response = self.llm.complete(prompt)
    return response

    strategies = get_reasoning(task)

    query = get_query(prompt, strategies)
    get_context()

    model_response: DeploymentResponse = self.llm.remote(prompt)
    # Pass the adder response directly into the multipler (no `await` needed).
    multiplier_response: DeploymentResponse = self._multiplier.remote(
        adder_response
    )
    # `await` the final chained response.
    return await multiplier_response
    def register(self):
        unity.tables('data.agents')


    def execute_task(self, Task) -> Result:
        self.status = "Running"
        self.status = "Running"
        self.logger.info(f"{timestamp.utc(now)}Agent {self.name} started task {Task.name} [{Task.id}]")

        return result


def get_status(self) -> AgentStatus:
    return self.status


def get_tools(self) -> List[BaseTool]:
    return self.tools


def select_tool(self, tools, criteria, strategy):

        print(self.tools)
