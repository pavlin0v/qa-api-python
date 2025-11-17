from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

class BaseResponse(BaseModel):
    id: int
    created_at: datetime

class TextField(BaseModel):
    text: str = Field(..., min_length=1, description="Text answer cannot be empty")
    
class QuestionResponse(BaseResponse, TextField):
    pass

class QuestionCreateRequest(TextField):
    pass

class AnswerResponse(BaseResponse, TextField):
    question_id: int
    user_id: UUID

class AnswerCreateRequest(TextField):
    user_id: UUID

class QuestionWithAnswersResponse(QuestionResponse):
    answers: list[AnswerResponse]
