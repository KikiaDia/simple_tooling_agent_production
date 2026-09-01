import asyncio
from dataclasses import dataclass

from simple_agent.backends import AgentBackend, AgentResult


@dataclass
class AgentService:
    backend: AgentBackend
    timeout_seconds: float

    async def ask(self, message: str) -> AgentResult:
        return await asyncio.wait_for(
            self.backend.invoke(message),
            timeout=self.timeout_seconds,
        )
