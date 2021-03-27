# All Django Stuff
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
from serase_app.utils import *
from serase_app.serializers import *
from serase_movimentacao.utils import calcular_saldo


# Views relacionadas ao Login

class CadastrarUsuarioView(APIView):

    def post (self,request):
        json_data = json.loads(request.body)

        required_params(json_data, ["email", "senha"])
        validacao = UserSerializer(data={"email": json_data['email'], "password":json_data['senha'] })
        validacao.is_valid(raise_exception=True)
        data = validacao.validated_data

        usuario = User.objects.create_user(email=data["email"],password=data["password"])
        usuario.save()
        token = Token.objects.create(user=usuario)

        return RespostaConteudo(200, {
            "nome": usuario.get_full_name(),
            "email": usuario.email,
            "token": "Token "+str(token),
        })      

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

        required_params(json_data, ["email", "senha"])
        validacao = ParametroUserSerializer(data=json_data)
        validacao.is_valid(raise_exception=True)

        usuario = authenticate(request, email=json_data["email"], password=json_data["senha"])

        if usuario is not None:
            token = Token.objects.get(user=usuario)

            return RespostaConteudo(200, {
                "nome": usuario.get_full_name(),
                "email": usuario.email,
                "token": "Token "+str(token),
            })
        else:
            return RespostaStatus(400, "Email ou senha invalidos!")    

class LogoutView(APIView):
             
    def get(self,request):
        logout(request)
        return RespostaStatus(200, "Logout realizado com sucesso!")
