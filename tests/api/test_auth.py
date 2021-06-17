from jose import jwt

from farfor_bot.api.dependencies import TokenPayloadSchema
from farfor_bot.config import settings
from farfor_bot.repositories import user_repository
from farfor_bot.security import ALGORITHM, get_password_hash
from tests.factories import UserFactory


def test_login(api_client, session):
    admin = UserFactory.create(
        is_superuser=False,
        is_admin=True,
        login="admin",
        hashed_password=get_password_hash("admin"),
    )

    # Авторизуемся под пользователем админа
    request_json = {"username": admin.login, "password": "admin"}
    response = api_client.post("/api/auth/login", request_json)

    access_token = response.json()["access_token"]

    # декодируем токен, на выходе должны получить id пользователя
    payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    token_data = TokenPayloadSchema(**payload)

    user = user_repository.get(db=session, id=token_data.user_id)

    assert response.status_code == 200
    assert user.login == admin.login


def test_auth_invalid_login(api_client, session):
    admin = UserFactory.create(
        is_superuser=False,
        is_admin=True,
        login="admin",
        hashed_password=get_password_hash("admin"),
    )
    request_json = {"username": "invalid", "password": "admin"}
    response = api_client.post("/api/auth/login", request_json)

    assert response.status_code == 400
    assert response.json() == {"detail": "Неправильный логин или пароль"}


def test_auth_invalid_password(api_client, session):
    admin = UserFactory.create(
        is_superuser=False,
        is_admin=True,
        login="admin",
        hashed_password=get_password_hash("admin"),
    )
    request_json = {"username": "admin", "password": "invalid"}
    json_response = api_client.post("/api/auth/login", request_json)

    assert json_response.status_code == 400
    assert json_response.json() == {"detail": "Неправильный логин или пароль"}


# def test_inactive(api_client, user, session):
#     request_json = {"username": user.login, "password": "user"}
#     response = api_client.post("/api/auth/login", request_json)
#
#     assert response.status_code == 400
#     assert response.json() == {"detail": "Пользователь деактивирован"}
