from typing import Dict, Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, Request


class BackendResponse(BaseModel):
    data: Optional[Dict] = Field(None, title="Primary response data.")


class MockBackendServer(FastAPI):

    def __init__(self):
        super().__init__(title='mock', version='0.0.1')

        @self.get('/{fn}', response_model=BackendResponse)
        def mock_backend(request: Request, fn: str) -> BackendResponse:
            return BackendResponse(data={'output': 'mock', 'function': fn})
