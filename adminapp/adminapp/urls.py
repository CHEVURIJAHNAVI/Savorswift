from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.projecthomepage,name='projecthomepage'),
    path('registerpagecall/',views.registerpagecall,name='registerpagecall'),
    path('registerpagelogic/',views.registerpagelogic,name='registerpagelogic'),
    path('loginpagecall/',views.loginpagecall,name='loginpagecall'),
    path('loginpagelogic/',views.loginpagelogic,name='loginpagelogic'),
    path('logout/',views.logout,name='logout'),
]