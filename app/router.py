from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Question, Answer
from app.schemas import (
    AnswerCreateRequest,
    AnswerResponse,
    QuestionCreateRequest,
    QuestionResponse,
    QuestionWithAnswersResponse,
)
from app.database import get_session

router = APIRouter()

@router.get(
    "/questions/", 
    response_model=list[QuestionResponse]
)
async def get_questions(
    session: AsyncSession = Depends(get_session)
) -> list[QuestionResponse]:
    questions = await session.scalars(
        select(Question)
        .limit(100)
    )

    return questions.all()

@router.post(
    "/questions/",
    response_model=QuestionResponse,
)
async def create_question(
    question: QuestionCreateRequest,
    session: AsyncSession = Depends(get_session)
) -> QuestionResponse:
    question = Question(text=question.text)
    session.add(question)
    await session.commit()
    await session.refresh(question)

    return QuestionResponse(
        id=question.id, 
        text=question.text, 
        created_at=question.created_at
    )

@router.get(
    "/questions/{question_id}",
    response_model=QuestionWithAnswersResponse
)
async def get_question_with_answers(
    question_id: int,
    session: AsyncSession = Depends(get_session)
) -> QuestionWithAnswersResponse:
    question = await session.scalar(
        select(Question)
        .where(Question.id == question_id)
    )

    if question is None:
        raise HTTPException(
            status_code=404, 
            detail="No question found"
        )
        
    answers = await session.scalars(
        select(Answer)
        .where(Answer.question_id == question_id)
        .limit(100)
    )

    answers_list = [
        AnswerResponse(
            id=answer.id,
            question_id=answer.question_id,
            text=answer.text,
            created_at=answer.created_at,
            user_id=answer.user_id,
        )
        for answer in answers.all()
    ]

    return QuestionWithAnswersResponse(
        id=question.id, 
        text=question.text, 
        created_at=question.created_at, 
        answers=answers_list
    )


@router.delete(
    "/questions/{question_id}",
)
async def delete_question(
    question_id: int,
    session: AsyncSession = Depends(get_session)
) -> None:
    question = await session.scalar(
        select(Question)
        .where(Question.id == question_id)
    )

    if question is None:
        raise HTTPException(
            status_code=404, 
            detail="No question found"
        )
    await session.delete(question)

    await session.commit()
    return {"message": "Question deleted successfully"}

@router.post(
    "/questions/{question_id}/answers/",
    response_model=AnswerResponse,
)
async def create_answer(
    question_id: int,
    answer: AnswerCreateRequest,
    session: AsyncSession = Depends(get_session)
) -> AnswerResponse:
    question = await session.scalar(
        select(Question)
        .where(Question.id == question_id)
    )

    if question is None:
        raise HTTPException(
            status_code=404, 
            detail="No question found"
        )

    answer = Answer(
        text=answer.text, 
        question=question, 
        user_id=answer.user_id
    )

    session.add(answer)
    await session.commit()
    await session.refresh(answer)

    return AnswerResponse(
        id=answer.id,
        text=answer.text,
        created_at=answer.created_at,
        question_id=answer.question_id,
        user_id=answer.user_id
    )

@router.get(
    "/answers/{answer_id}",
    response_model=AnswerResponse,
)
async def get_answer(
    answer_id: int,
    session: AsyncSession = Depends(get_session)
) -> AnswerResponse:
    answer = await session.scalar(
        select(Answer)
        .where(Answer.id == answer_id)
    )

    if answer is None:
        raise HTTPException(
            status_code=404, 
            detail="No answer found"
        )

    return AnswerResponse(
        id=answer.id,
        text=answer.text,
        created_at=answer.created_at,
        question_id=answer.question_id,
        user_id=answer.user_id
    )

@router.delete("/answers/{answer_id}")
async def delete_answer(
    answer_id: int,
    session: AsyncSession = Depends(get_session)
):
    answer = await session.scalar(
        select(Answer).where(Answer.id == answer_id)
    )

    if answer is None:
        raise HTTPException(
            status_code=404,
            detail="No answer found"
        )

    await session.delete(answer)
    await session.commit()

    return {"message": "Answer deleted successfully"}
