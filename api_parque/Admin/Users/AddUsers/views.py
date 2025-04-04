from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api_parque.models import User, TypeUser
from rest_framework.permissions import IsAuthenticated
from api_parque.Admin.Users.AddUsers.serializers import RegisterUsersSerializer
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.template import TemplateDoesNotExist
from django.utils.crypto import get_random_string

class AddUserAPiView(APIView):
    
 

    def post(self, request): 
        user = request.user
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        age = request.data.get('age', '')
        phone = request.data.get('phone', '')
        email = request.data.get('email', '')
        type_user = int(request.data.get('type_user', 0))
        random_password = get_random_string(12)

        id_type = TypeUser.objects.get(id=type_user)
        try:
            user_exist = User.objects.filter(username=email).exists()   
            if user_exist:
                return Response({'error': 'this email has already User'}, status=status.HTTP_400_BAD_REQUEST)
                 
            if id_type:

                user = User(first_name=first_name, 
                            last_name=last_name,
                            age=age,
                            phone=phone,
                            email=email,
                            password=random_password,
                            type_id=id_type,
                            username=email
                        )
                
                user.set_password(random_password)
                context = {
                    'userName': email,
                    'userPass': random_password
                    }
                try:
                    template = get_template('Welcome.html').render(context)
                except TemplateDoesNotExist:
                        print("Error: La plantilla 'Welcome.html' no se encontró.")
                        raise
                    
                    # Crear el objeto de correo electrónico
                email_message = EmailMessage(
                    subject='No reply: Registro exitoso',   # Asunto del correo
                    body=template,                                      # Cuerpo del correo en formato HTML
                    from_email='marco.vallejo2000@gmail.com',                 # Remitente del correo
                    to=[email],                                         # Destinatario principal (utiliza el email obtenido)
                )

                # Especificar que el cuerpo del mensaje es HTML
                email_message.content_subtype = "html"

                # Enviar el correo
                try:
                    email_message.send(fail_silently=False)
                    print("Correo enviado correctamente.")
                except Exception as e:
                    print(f"Error al enviar el correo: {e}")
                    raise
                user.save()
                
                return Response({'message': 'user was created successfully'}, status=status.HTTP_201_CREATED)

        except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self, request):
        
        request.user

        try:

            users = User.objects.all()
            serializer = RegisterUsersSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except users.DoesNotExist:
            return Response({'error': 'There is no Users in table'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete (self, request):
        user = request.user
        id = request.data.get('id', None)

        if not id:
            return Response({'message': 'id is required to delete a user'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
        
            user = User.objects.get(id=id)
            user.delete()

            return Response({'message': 'user User was deleted successfully'}, status=status.HTTP_200_OK)
        
        except user.DoesNotExist:
            return Response({'error': 'There is no Users in table'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'message': str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put (self, request):
        user = request.user
        id = request.data.get('id', None)
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', None)
        age = request.data.get('age', '')
        email = request.data.get('email', '')
        phone = request.data.get('phone', '')
        type_id = request.data.get('type_id', '')

        
        type_id = TypeUser.objects.get(id=type_id)

        if not id:
            return Response({'message': 'id is required to delete a User'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
        
            user = User.objects.get(id=id)
            user.first_name = first_name
            user.scientific_name = last_name
            user.age = age
            user.email = email
            user.phone = phone
            user.type_id=type_id
            user.save()

            return Response({'message': 'User updated successfully'}, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
        except TypeUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
        except Exception as e:
            return Response({'message': str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                 


    
         