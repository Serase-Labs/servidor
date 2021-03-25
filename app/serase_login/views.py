# All Django Stuff
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

# All rest framework stuff
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

# All python and dependences stuff
import json

# All in other app stuff
from serase_app.models import *
from serase_app.padroes_resposta import *



# Views relacionadas ao Login

class CadastrarUsuarioView(APIView):

    def post (self,request):
        
        json_data = json.loads(request.body)
        nome = json_data['nome']
        email=json_data['email']
        senha = json_data['senha'] 
        aux_usuario=User.objects.filter(email=email)

        if aux_usuario:
            return RespostaStatus(400,"Erro! Usario já cadastrado")

    
        novo_usuario = User.objects.create_user(username=nome,email=email,password=senha)
        novo_usuario.save()
        Token.objects.create(user=novo_usuario)

        return RespostaStatus(200, "Requisição feita com sucesso!")        

class UsuarioLogadoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        username = None
        if request.user.is_authenticated:
            username = request.user.get_username()
            return RespostaStatus(200, username)  
        else:
            return RespostaStatus(400, "Senha ou usuario invalidos ")

class InformacoesUsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuario = request.user
        s, saldo_total = calcular_saldo(usuario)

        return RespostaConteudo(200, {
            "nome": usuario.get_full_name(),
            "email": usuario.email,
            "saldo": round(saldo_total, 2),
        })

class LoginView(APIView):

    def post(self,request):
        json_data = json.loads(request.body)
        email=json_data['email']
        senha = json_data['senha']
        usuario= User.objects.get(email=email)
        nome = usuario.get_username()
        user = authenticate(request, username=nome, password=senha)
        
        
        if user is not None:
            login(request, user)
            token = Token.objects.get(user=usuario)

            return RespostaConteudo(200, {
                "nome": usuario.get_full_name(),
                "email": usuario.email,
                "token": "Token "+str(token),
            })
        else:
            return RespostaStatus(400, "Senha ou usuario invalidos!")    

class LogoutView(APIView):
             
    def get(self,request):
        logout(request)
        return RespostaStatus(200, "Requisição feita com sucesso!")
