from django.urls import path, include
from .views import *
from serase_app.views import StatusServidorView

# Para acessar as urls deste arquivo, adicione na frente "relatorio/", por exemplo conseguimos acessar a url "categoria" através de "relatorio/categoria"
urlpatterns = [
    path('status/', StatusServidorView.as_view(), name='status_teste'),
]
