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

class DividaSerializer (serializers.ModelSerializer):
    class Meta:
        model = Divida
        fields = '__all__'


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


class FiltrarCobrancaSerializer(serializers.Serializer):
    tipo = serializers.CharField(max_length=7, required=False)
    situacao = serializers.CharField(max_length=8, required=False)
    cod_padrao = serializers.IntegerField(required=False)

    def validate_tipo(self, value):
        TIPO_MOVIMENTACAO = ["receita","despesa"]
        if value not in TIPO_MOVIMENTACAO:
            raise serializers.ValidationError("Tipo não aceita o valor '"+value+"'. Os valores aceitos são: "+", ".join(TIPO_MOVIMENTACAO))
        return value

    def validate_situacao(self, value):
        TIPO_MOVIMENTACAO = ["pendente","paga"]
        if value not in TIPO_MOVIMENTACAO:
            raise serializers.ValidationError("Tipo não aceita o valor '"+value+"'. Os valores aceitos são: "+", ".join(TIPO_MOVIMENTACAO))
        return value
    
    def validate_cod_padrao(self, value):
        if not PadraoMovimentacao.objects.filter(id=value).exists():
             raise serializers.ValidationError("Padrão inexistente!")
        return PadraoMovimentacao.objects.get(id=value)

class PagarCobrancaSerializer(serializers.Serializer):
    valor_pago = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)



class ParametroDividaSerializer(serializers.ModelSerializer):
    categoria = serializers.CharField(max_length=20, required=False)
    periodo = serializers.CharField(max_length=7, required=False)
    dia_cobranca = serializers.IntegerField(required=False)
    data_fim = serializers.DateField(required=False)

    def validate_juros_tipo(self, value):
        TIPO_JUROS = ["composto","simples"]
        if value not in TIPO_JUROS:
            raise serializers.ValidationError("Tipo não aceita o valor '"+value+"'. Os valores aceitos são: "+", ".join(TIPO_JUROS))
        return value


    def validate_categoria(self, value):
        if not Categoria.objects.filter(nome=value).exists():
             raise serializers.ValidationError("Categoria inexistente!")
        return Categoria.objects.get(nome=value)

    class Meta:
        model = Divida
        fields = '__all__'

class FiltrarDividaSerializer(serializers.Serializer):
    categoria = serializers.CharField(max_length=20, required=False)
    juros_tipo = serializers.CharField(max_length=8, required=False)
    juros_ativos = serializers.BooleanField(required=False)
    quitada = serializers.BooleanField(required=False)

    def validate_juros_tipo(self, value):
        TIPO_JUROS = ["composto","simples"]
        if value not in TIPO_JUROS:
            raise serializers.ValidationError("Tipo não aceita o valor '"+value+"'. Os valores aceitos são: "+", ".join(TIPO_JUROS))
        return value
    
    def validate_categoria(self, value):
        if not Categoria.objects.filter(nome=value).exists():
             raise serializers.ValidationError("Categoria inexistente!")
        return Categoria.objects.get(nome=value)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')

class ParametroUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    senha = serializers.CharField(max_length=128, write_only=True)