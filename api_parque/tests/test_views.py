import pytest
from rest_framework.test import APIClient, APIRequestFactory
from django.urls import reverse
from api_parque.models import Habitat, TypeUser, User
from api_parque.Admin.Habitat.views import HabitatAPiView

@pytest.mark.django_db
def test_create_habitat_api(monkeypatch):
    """
    Prueba el endpoint POST de Habitat
    """
    client = APIClient()
    tipo = TypeUser.objects.create(type_user="Admin")
    user = User.objects.create_user(
        username="admin",
        password="12345",
        first_name="Admin",
        last_name="User",
        age="1990-01-01",
        phone="5555555",
        email="admin@example.com",
        type_id=tipo,
    )
    client.force_authenticate(user=user)

    # Simular archivo subido
    class FileMock:
        name = "test.jpg"
        content_type = "image/jpeg"

    file_mock = FileMock()

    # Simular función upload_to_s3 para no depender de AWS real
    def fake_upload(file, folder):
        return {"key": "fake_photo.jpg"}

    monkeypatch.setattr("api_parque.Admin.Habitat.views.upload_to_s3", fake_upload)

    url = reverse("add-habitat")  # Ajusta según tu urls.py
    data = {
        "name": "Bosque",
        "photo": file_mock
    }
    response = client.post(url, data, format="multipart")
    assert response.status_code == 201
    assert response.data["photo_url"] == "fake_photo.jpg"
    assert Habitat.objects.count() == 1


@pytest.mark.django_db
def test_get_habitat_list_api():
    """
    Prueba el endpoint GET de Habitat
    """
    client = APIClient()
    tipo = TypeUser.objects.create(type_user="Admin")
    user = User.objects.create_user(
        username="admin2",
        password="12345",
        first_name="Admin",
        last_name="User",
        age="1990-01-01",
        phone="5555555",
        email="admin2@example.com",
        type_id=tipo,
    )
    client.force_authenticate(user=user)

    Habitat.objects.create(name="Selva", photo="selva.jpg")
    url = reverse("add-habitat")
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == "Selva"


@pytest.mark.django_db
def test_update_habitat_api():
    """
    Prueba el endpoint PUT de Habitat
    """
    client = APIClient()
    tipo = TypeUser.objects.create(type_user="Admin")
    user = User.objects.create_user(
        username="admin3",
        password="12345",
        first_name="Admin",
        last_name="User",
        age="1990-01-01",
        phone="5555555",
        email="admin3@example.com",
        type_id=tipo,
    )
    client.force_authenticate(user=user)

    habitat = Habitat.objects.create(name="Montaña", photo="montana.jpg")
    url = reverse("add-habitat")
    data = {
        "id": habitat.id,
        "name": "Montaña actualizada",
        "photo": "montana2.jpg"
    }
    response = client.put(url, data, format="json")
    assert response.status_code == 200
    habitat.refresh_from_db()
    assert habitat.name == "Montaña actualizada"
    assert habitat.photo == "montana2.jpg"


@pytest.mark.django_db
def test_delete_habitat_api():
    """
    Prueba el endpoint DELETE de Habitat
    """
    client = APIClient()
    tipo = TypeUser.objects.create(type_user="Admin")
    user = User.objects.create_user(
        username="admin4",
        password="12345",
        first_name="Admin",
        last_name="User",
        age="1990-01-01",
        phone="5555555",
        email="admin4@example.com",
        type_id=tipo,
    )
    client.force_authenticate(user=user)

    habitat = Habitat.objects.create(name="Desierto", photo="desierto.jpg")
    url = reverse("add-habitat")
    data = {"id": habitat.id}
    response = client.delete(url, data, format="json")
    assert response.status_code == 200
    assert Habitat.objects.count() == 0
