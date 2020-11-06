from django.db import models

# Create your models here.
Class Usuario(models.model):
    cod_user=models.CharField(max_length=10, primary_key= true )#AutoField(primary_key=True)
    email= models.EmailField(max_length = 200) 
    senha =models.CharField(max_length =30)
    

Class Saldo(models.model)
   
    cod_user=models.ForeignKey(Usuario, on_delete=models.CASCADE)
    mes_ano=  models.IntegerField()#similar a periodo
    saldo= models.DecimalField(decimal_places=2)
    
    
Class Movimentacao(models.model)
    cod_movimentacao=models.AutoField(primary_key=True)
    data =models.DateField()
    valor_a _pagar= models.DecimalField(decimal_places=2)
    dat_geracao= models.DateField
    data_geracao=models.DateField
    valor_pago= models.DecimalField(decimal_places=2)
    cod_user=cod_user=models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cod_cat =models.ForeingKey(Categoria,on_delete=models.CASCADE )

Class Categoria(models.model)
    cod_cat =models.AutoField(primary_key=True)
    nome_cat =models.CharField(max_length=2)
    
Class PadraoMovimentacao(models.model)
    cod_padrao=AutoField(primary_key=True)
    receitaDespesa=models.BooleanField()
    descricao=models.TextField()
    periodo =  models.IntegerField()
    valor=models.DecimalField(decimal_places=2)
    dia_cobranca-models.DateField()
    dat_inicio=models.DateField()
    dat_fim= models.DateField()
    cod_user=cod_user=models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cod_cat =models.ForeingKey(Categoria,on_delete=models.CASCADE )

    
    