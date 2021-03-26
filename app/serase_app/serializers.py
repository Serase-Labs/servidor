from django.contrib.auth.models import User
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


# Validadores

class ParametroMovimentacaoSerializer(serializers.ModelSerializer):
    categoria = serializers.CharField(max_length=20, required=False)

    def validate_categoria(self, value):
        if not Categoria.objects.filter(nome=value).exists():
             raise serializers.ValidationError("Categoria inexistente!")
        return value

    class Meta:
        model = Movimentacao
        fields = ['descricao', 'valor_pago', 'data_lancamento', 'categoria']

class FiltrarMovimentacaoSerializer(serializers.Serializer):
    categoria = serializers.CharField(max_length=20, required=False)
    tipo = serializers.CharField(max_length=7, required=False)
    data_inicial = serializers.DateField(required=False)
    data_final = serializers.DateField(required=False)


    def validate_tipo(self, value):
        TIPO_MOVIMENTACAO = ["receita","despesa"]
        if value not in TIPO_MOVIMENTACAO:
            raise serializers.ValidationError("Tipo não aceita o valor '"+value+"'. Os valores aceitos são: "+", ".join(TIPO_MOVIMENTACAO))
        return value

    def validate_categoria(self, value):
        if not Categoria.objects.filter(nome=value).exists():
             raise serializers.ValidationError("Categoria inexistente!")
        return Categoria.objects.get(nome=value)

class ParametroPadraoMovimentacaoSerializer(serializers.ModelSerializer):
    tipo = serializers.CharField(max_length=7, required=False)
    categoria = serializers.CharField(max_length=20, required=False)
    periodo = serializers.CharField(max_length=7, required=False)
    dia_cobranca = serializers.IntegerField(required=False)

    def validate_tipo(self, value):
        TIPO_PADRAO = ["receita","despesa"]
        if value not in TIPO_PADRAO:
            raise serializers.ValidationError("Tipo não aceita o valor '"+value+"'. Os valores aceitos são: "+", ".join(TIPO_PADRAO))
        return value

    def validate_categoria(self, value):
        if not Categoria.objects.filter(nome=value).exists():
             raise serializers.ValidationError("Categoria inexistente!")
        return Categoria.objects.get(nome=value)

    class Meta:
        model = PadraoMovimentacao
        fields = ["tipo", "descricao", "periodo", "valor", "dia_cobranca", "data_fim", "categoria"]

class FiltrarPadraoMovimentacaoSerializer(serializers.Serializer):
    categoria = serializers.CharField(max_length=20, required=False)
    tipo = serializers.CharField(max_length=7, required=False)

    def validate_tipo(self, value):
        TIPO_MOVIMENTACAO = ["receita","despesa"]
        if value not in TIPO_MOVIMENTACAO:
            raise serializers.ValidationError("Tipo não aceita o valor '"+value+"'. Os valores aceitos são: "+", ".join(TIPO_MOVIMENTACAO))
        return value

    def validate_categoria(self, value):
        if not Categoria.objects.filter(nome=value).exists():
             raise serializers.ValidationError("Categoria inexistente!")
        return Categoria.objects.get(nome=value)