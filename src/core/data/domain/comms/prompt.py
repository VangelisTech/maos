from typing import Optional, List, Any
from pydantic import Field
from src.core.data.schema.base import DomainObject, DomainFactory, DomainSelector, DomainObjectAccessor
from api.config import Config

class Prompt(DomainObject):
    name: Optional[str] = Field(default=None, description="Name of the prompt")
    contents: Optional[List[Any]] = Field(default=None, description="Contents of the prompt")
    system_prompt: Optional[str] = Field(default=None, description="System prompt")
    max_tokens: Optional[int] = Field(default=None, description="Maximum number of tokens")
    max_length: Optional[int] = Field(default=None, description="Maximum length of the prompt")
    temperature: Optional[float] = Field(default=None, description="Temperature for text generation")
    top_k: Optional[float] = Field(default=None, description="Top-k sampling parameter")
    top_p: Optional[float] = Field(default=None, description="Top-p sampling parameter")
    seed: Optional[int] = Field(default=None, description="Random seed for text generation")
    stop_token: Optional[str] = Field(default=None, description="Stop token for text generation")

    class Meta:
        type: str = "Prompt"

class PromptFactory(DomainFactory[Prompt]):
    @staticmethod
    def create_new_prompt(
        name: Optional[str] = None,
        contents: Optional[List[Any]] = None,
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None,
        max_length: Optional[int] = None,
        temperature: Optional[float] = None,
        top_k: Optional[float] = None,
        top_p: Optional[float] = None,
        seed: Optional[int] = None,
        stop_token: Optional[str] = None
    ) -> Prompt:
        return Prompt.create_new(
            name=name,
            contents=contents,
            system_prompt=system_prompt,
            max_tokens=max_tokens,
            max_length=max_length,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            seed=seed,
            stop_token=stop_token
        )

class PromptSelector(DomainSelector):
    @staticmethod
    def by_name(name: str) -> str:
        return f"{PromptSelector.base_query('prompts')} WHERE name = '{name}'"

    @staticmethod
    def by_system_prompt(system_prompt: str) -> str:
        return f"{PromptSelector.base_query('prompts')} WHERE system_prompt = '{system_prompt}'"

class PromptAccessor(DomainObjectAccessor):
    def __init__(self, config: Config):
        super().__init__(config)

    async def get_prompt_by_name(self, name: str) -> Optional[Prompt]:
        query = PromptSelector.by_name(name)
        df = self.config.daft().sql(query)
        if df.count().collect()[0] > 0:
            prompt_data = df.collect().to_pydict()[0]
            return PromptFactory.create_from_data(prompt_data, "Prompt")
        return None

    async def get_prompts_by_system_prompt(self, system_prompt: str) -> List[Prompt]:
        query = PromptSelector.by_system_prompt(system_prompt)
        df = self.config.daft().sql(query)
        prompts_data = df.collect().to_pydict()
        return [PromptFactory.create_from_data(data, "Prompt") for data in prompts_data]

    async def create_prompt(self, **prompt_data) -> Prompt:
        new_prompt = PromptFactory.create_new_prompt(**prompt_data)
        # Here you would typically insert the new prompt into the Iceberg table
        # For this example, we'll just return the new prompt
        return new_prompt

    async def update_prompt(self, prompt: Prompt) -> Prompt:
        prompt.update_timestamp()
        # Here you would typically update the prompt in the Iceberg table
        # For this example, we'll just return the updated prompt
        return prompt

    async def delete_prompt(self, prompt_id: str) -> bool:
        # Here you would typically delete the prompt from the Iceberg table
        # For this example, we'll just return True
        return await self.delete("prompts", prompt_id, "Prompt")