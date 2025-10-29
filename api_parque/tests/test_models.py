
# import pytest
# from django.utils import timezone
# from api_parque.models import (
#     TypeUser, TypeRegister, Status, User, Register, Habitat, RegisterHabitat,
#     Threat, RegisterThreat, Sighting, Alimentation, RegisterAlimentation,
#     Distribution, RegisterDistribution, Comments, PageVisit
# )

# @pytest.mark.django_db
# def test_create_type_user():
#     tipo = TypeUser.objects.create(type_user="Administrador")
#     assert tipo.id is not None
#     assert str(tipo.type_user) == "Administrador"


# @pytest.mark.django_db
# def test_create_user_with_type_user():
#     tipo = TypeUser.objects.create(type_user="Investigador")
#     user = User.objects.create_user(
#         username="testuser",
#         password="12345",
#         first_name="Juan",
#         last_name="Pérez",
#         age="2000-01-01",
#         phone="555-5555",
#         email="juan@example.com",
#         type_id=tipo,
#     )
#     assert user.username == "testuser"
#     assert user.type_id.type_user == "Investigador"


# @pytest.mark.django_db
# def test_create_register_and_status():
#     status = Status.objects.create(status="En peligro")
#     type_reg = TypeRegister.objects.create(type_register="Fauna")
#     reg = Register.objects.create(
#         name="Jaguar",
#         scientific_name="Panthera onca",
#         function="Depredador tope",
#         description="Felino americano",
#         habitat="Selva",
#         distribution="América Latina",
#         sound="Rugido fuerte",
#         photo="jaguar.jpg",
#         video="jaguar.mp4",
#         type_id=type_reg,
#         status_id=status
#     )
#     assert reg.scientific_name == "Panthera onca"
#     assert reg.status_id.status == "En peligro"


# @pytest.mark.django_db
# def test_register_habitat_relationship():
#     status = Status.objects.create(status="Amenazado")
#     type_reg = TypeRegister.objects.create(type_register="Flora")
#     reg = Register.objects.create(
#         name="Encino",
#         scientific_name="Quercus",
#         function="Árbol importante",
#         description="Árbol de zonas templadas",
#         habitat="Bosques",
#         distribution="México",
#         sound="N/A",
#         photo="encino.jpg",
#         video="encino.mp4",
#         type_id=type_reg,
#         status_id=status
#     )
#     habitat = Habitat.objects.create(name="Bosque", description="Área boscosa", photo="bosque.jpg")
#     RegisterHabitat.objects.create(register=reg, habitat=habitat)

#     assert habitat.register.first().name == "Encino"


# @pytest.mark.django_db
# def test_register_threat_relationship():
#     status = Status.objects.create(status="Crítico")
#     type_reg = TypeRegister.objects.create(type_register="Fauna")
#     reg = Register.objects.create(
#         name="Águila Real",
#         scientific_name="Aquila chrysaetos",
#         function="Ave nacional",
#         description="Ave rapaz",
#         habitat="Montañas",
#         distribution="México",
#         sound="Chillido",
#         photo="aguila.jpg",
#         video="aguila.mp4",
#         type_id=type_reg,
#         status_id=status
#     )
#     threat = Threat.objects.create(name="Caza furtiva")
#     RegisterThreat.objects.create(register=reg, threat=threat)

#     assert reg.threats.first().name == "Caza furtiva"


# @pytest.mark.django_db
# def test_sighting_creation():
#     status = Status.objects.create(status="Vulnerable")
#     type_reg = TypeRegister.objects.create(type_register="Fauna")
#     reg = Register.objects.create(
#         name="Venado Cola Blanca",
#         scientific_name="Odocoileus virginianus",
#         function="Herbívoro",
#         description="Mamífero común",
#         habitat="Bosques",
#         distribution="América",
#         sound="N/A",
#         photo="venado.jpg",
#         video="venado.mp4",
#         type_id=type_reg,
#         status_id=status
#     )
#     sighting = Sighting.objects.create(
#         description="Avistamiento en el bosque",
#         photo="venado.jpg",
#         type_register=type_reg,
#         sighting_name=reg,
#         full_name="Carlos López"
#     )
#     assert sighting.validated is False
#     assert sighting.sighting_name.name == "Venado Cola Blanca"


# @pytest.mark.django_db
# def test_page_visit_creation():
#     user_type = TypeUser.objects.create(type_user="Visitante")
#     user = User.objects.create_user(
#         username="visitante",
#         password="pass123",
#         first_name="Ana",
#         last_name="Martínez",
#         age="1990-05-05",
#         phone="123456789",
#         email="ana@example.com",
#         type_id=user_type,
#     )
#     visit = PageVisit.objects.create(
#         path="/home",
#         ip_address="127.0.0.1",
#         user_agent="Mozilla",
#         user=user
#     )
#     assert visit.path == "/home"
#     assert visit.user.username == "visitante"
#     assert isinstance(visit.timestamp, timezone.datetime)

