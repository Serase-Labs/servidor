
from django.contrib.auth.models import User # import user model
from rest_framework import serializers
from .models import *

# Create member serializer
class PadraoMovimentacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PadraoMovimentacao
        fields = '__all__'
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class MovimentacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimentacao
        fields = '__all__'
class SaldoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saldo
        fields = '__all__'
class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model= User
        fields='__all__'