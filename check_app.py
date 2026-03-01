from fastapi.testclient import TestClient

from app import api, feedbacks


client = TestClient(api)


def run_checks() -> None:
    feedbacks.clear()

    browser_response = client.get("/", headers={"accept": "text/html"})
    assert browser_response.status_code == 200
    assert "ВСЕМ, ПРИВЕТ!" in browser_response.text

    api_response = client.get("/", headers={"accept": "application/json"})
    assert api_response.status_code == 200
    assert api_response.json() == {"message": "Добро пожаловать в моё приложение FastAPI!"}

    calc_query = client.post("/calculate?num1=5&num2=10")
    assert calc_query.status_code == 200
    assert calc_query.json() == {"result": 15}

    calc_body = client.post("/calculate", json={"num1": 2.5, "num2": 3.5})
    assert calc_body.status_code == 200
    assert calc_body.json() == {"result": 6}

    user_response = client.get("/users")
    assert user_response.status_code == 200
    assert user_response.json() == {
        "name": "Ладинский Александр Владимирович",
        "id": 1,
    }

    adult_response = client.post("/user", json={"name": "Александр", "age": 18})
    assert adult_response.status_code == 200
    assert adult_response.json() == {
        "name": "Александр",
        "age": 18,
        "is_adult": True,
    }

    feedback_response = client.post(
        "/feedback",
        json={
            "name": "Александр",
            "message": "Это непросто, но я всё сделаю правильно.",
        },
    )
    assert feedback_response.status_code == 200
    assert feedback_response.json() == {
        "message": "Спасибо, Александр! Ваш отзыв сохранён."
    }
    assert len(feedbacks) == 1

    invalid_response = client.post(
        "/feedback",
        json={
            "name": "А",
            "message": "Какой-то кринж у вас тут происходит...",
        },
    )
    assert invalid_response.status_code == 422

    print("Все проверки пройдены.")


if __name__ == "__main__":
    run_checks()
