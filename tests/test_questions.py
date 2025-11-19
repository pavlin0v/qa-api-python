import pytest
from httpx import AsyncClient

from tests.conftest import (
    default_question_text,
    default_answer_text,
    default_user_id,
)


@pytest.mark.asyncio
async def test_create_question(client: AsyncClient):
    """Test creating a question"""
    response = await client.post(
        "/questions/",
        json={
            "text": default_question_text,
        },
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == default_question_text
    assert data["created_at"] is not None
    assert data["id"] is not None


@pytest.mark.asyncio
async def test_get_questions_returns_list(client: AsyncClient):
    """Test getting questions returns a list"""
    
    response = await client.get("/questions/")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_questions_with_data(client: AsyncClient):
    """Test getting a list of questions"""
    await client.post(
        "/questions/",
        json={"text": default_question_text},
    )
    
    response = await client.get("/questions/")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["text"] == default_question_text


@pytest.mark.asyncio
async def test_get_question_by_id(client: AsyncClient):
    """Test getting a question by ID"""
    create_response = await client.post(
        "/questions/",
        json={"text": default_question_text},
    )
    question_id = create_response.json()["id"]
    
    response = await client.get(f"/questions/{question_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == question_id
    assert data["text"] == default_question_text
    assert data["answers"] == []


@pytest.mark.asyncio
async def test_get_nonexistent_question(client: AsyncClient):
    """Test getting a nonexistent question"""
    response = await client.get("/questions/9999")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "No question found"


@pytest.mark.asyncio
async def test_delete_question(client: AsyncClient):
    """Test deleting a question"""
    create_response = await client.post(
        "/questions/",
        json={"text": default_question_text},
    )
    question_id = create_response.json()["id"]
    
    delete_response = await client.delete(f"/questions/{question_id}")
    
    assert delete_response.status_code == 200
    
    get_response = await client.get(f"/questions/{question_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_create_answer(client: AsyncClient):
    """Test creating an answer to a question"""
    question_response = await client.post(
        "/questions/",
        json={"text": default_question_text},
    )
    question_id = question_response.json()["id"]
    
    answer_response = await client.post(
        f"/questions/{question_id}/answers/",
        json={
            "text": default_answer_text,
            "user_id": default_user_id,
        },
    )
    
    assert answer_response.status_code == 200
    data = answer_response.json()
    assert data["text"] == default_answer_text
    assert data["user_id"] == default_user_id
    assert data["question_id"] == question_id
    assert data["id"] is not None


@pytest.mark.asyncio
async def test_create_answer_for_nonexistent_question(client: AsyncClient):
    """Test creating an answer for a nonexistent question"""
    response = await client.post(
        "/questions/9999/answers/",
        json={
            "text": default_answer_text,
            "user_id": default_user_id,
        },
    )
    
    assert response.status_code == 404
    assert response.json()["detail"] == "No question found"


@pytest.mark.asyncio
async def test_get_question_with_answers(client: AsyncClient):
    """Test getting a question with answers"""
    question_response = await client.post(
        "/questions/",
        json={"text": default_question_text},
    )
    question_id = question_response.json()["id"]
    
    await client.post(
        f"/questions/{question_id}/answers/",
        json={"text": "Ответ 1", "user_id": default_user_id},
    )
    await client.post(
        f"/questions/{question_id}/answers/",
        json={"text": "Ответ 2", "user_id": default_user_id},
    )
    
    response = await client.get(f"/questions/{question_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == question_id
    assert len(data["answers"]) == 2
    assert data["answers"][0]["text"] == "Ответ 1"
    assert data["answers"][1]["text"] == "Ответ 2"


@pytest.mark.asyncio
async def test_get_answer_by_id(client: AsyncClient):
    """Test getting an answer by ID"""
    question_response = await client.post(
        "/questions/",
        json={"text": default_question_text},
    )
    question_id = question_response.json()["id"]
    
    answer_response = await client.post(
        f"/questions/{question_id}/answers/",
        json={"text": default_answer_text, "user_id": default_user_id},
    )
    answer_id = answer_response.json()["id"]
    
    get_response = await client.get(f"/answers/{answer_id}")
    
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["id"] == answer_id
    assert data["text"] == default_answer_text


@pytest.mark.asyncio
async def test_delete_answer(client: AsyncClient):
    """Test deleting an answer"""
    question_response = await client.post(
        "/questions/",
        json={"text": default_question_text},
    )
    question_id = question_response.json()["id"]
    
    answer_response = await client.post(
        f"/questions/{question_id}/answers/",
        json={"text": default_answer_text, "user_id": default_user_id},
    )
    answer_id = answer_response.json()["id"]
    
    delete_response = await client.delete(f"/answers/{answer_id}")
    
    assert delete_response.status_code == 200
    
    get_response = await client.get(f"/answers/{answer_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_question_cascades_to_answers(client: AsyncClient):
    """Test cascading deletion of answers when a question is deleted"""
    question_response = await client.post(
        "/questions/",
        json={"text": default_question_text},
    )
    question_id = question_response.json()["id"]
    
    answer_response = await client.post(
        f"/questions/{question_id}/answers/",
        json={"text": default_answer_text, "user_id": default_user_id},
    )
    answer_id = answer_response.json()["id"]
    
    await client.delete(f"/questions/{question_id}")
    
    answer_get_response = await client.get(f"/answers/{answer_id}")
    assert answer_get_response.status_code == 404

