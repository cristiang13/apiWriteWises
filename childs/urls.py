from . import views
from django.urls import path
from .views import AddChild,GetChilds

urlpatterns = [
    path('add-child/', AddChild.as_view(), name='add_child'),
    path('get-childs/', GetChilds.as_view(), name='get_childs'),
  
]