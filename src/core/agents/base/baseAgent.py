from enum import Enum

import daft
import pyarrow as pa
from maf.core.schema.base import CustomModel
from pydantic import Field
from ray import serve
from ray.serve.handle import DeploymentHandle, DeploymentResponse

from maf.core.components.tools import BaseTool


class AgentStatus(str, Enum):
    IDLE = "idle"
    PENDING = "pending"
    WAITING = "waiting"
    PROCESSING = "processing"


@serve.deployment
class mmAgent(CustomModel):
    name: Optional[str] = Field(default_factory=RandomName(1)),
    status: AgentStatus = "Idle"
    mmllm: Optional[BaselLLM] = Field(default=MultiModalLLM(), description="The Multimodal Model"), no
    reasoning: Optional[DeploymentHandle] = Field(default=MultiModalLLM(), description="The embedding model"),
    memory: Optional[DeploymentHandle] = Field(
        default=VectorMemory(
            db=LanceDB(

            ),
            english=,
            multilingual=,
            multimodal=,
            transcription=,
            diarization=,
        ),
        description="The embedding model", ),
    embedding: Optional[DeploymentHandle] = Field(default=MultiModalEmbedding(), description="The embedding model"),
    speech:
            logs: daft.DataType.embedding
            metrics:
            tools: Optional[pa.list_[BaseTool]]
    ):
    super().(__init__(metadata=))
        self.name =  str
    self.models = model
    self.
    self.embedding = embedding
    self.tools = pa.list_()
    self.memory = self.get_query_pipelines()

    self.settings.MAX_NUM_PENDING_TASKS = 100
    self.settings.MAX_CONCURRENT_TASKS = 10


def __call__(self, request: Request, task: Task):
    prompt = Request.Prompt
    response = self.llm.complete(prompt)
    return response

    strategies = get_reasoning(task)

    query = get_query(prompt, strategies)
    get_context()

    model_response: DeploymentResponse = self.model.remote(prompt)
    # Pass the adder response directly into the multipler (no `await` needed).
    multiplier_response: DeploymentResponse = self._multiplier.remote(
        adder_response
    )
    # `await` the final chained response.
    return await multiplier_response
    def register(self):
        unity.tables('data.agents')


def refresh(self):
    unity = get_unity()
    ray = get_ray()
    daft = get_daft()

    def process(self):


def execute_task(self, Task) -> Result,


Action:
self.status = "Running"
self.logger.info(f"{timestamp.utc(now)}Agent {self.name} started task {Task.name} [{Task.id}]")

return result


def get_status(self) -> AgentStatus:
    return self.status


def get_tools(self) -> List[BaseTool]:
    return self.tools


def select_tool(self, tools, criteria, strategy):

        print(self.tools)
