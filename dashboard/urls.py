from django.urls import path
from . import views

urlpatterns = [
    path('create_profile/', views.index ,name='profile'),
    path('', views.home ,name='dashboard'),
    path('dashboard', views.conecte ,name='dashboardc'),

    path('fix_profile/', views.create ,name='profile_fixed'),
    path('edit_profile/', views.edit ,name='profile_edit'),
    path('choix_analyse/<str:nom>,<str:prenom>,<str:sexe>,<str:date>,<str:email>,<str:ville>,<str:contact>', views.choix ,name='choix_analyse'),

    path('v/<int:id>',views.opencam,name='video'),
    path('1/<str:file>,<int:id>',views.video,name='video1'),
    path('streaming/<int:id>',views.streaming,name='streaming_open'),
    path('analyse/<int:id>',views.analyse,name='analyse'),

    path('profile_show/<int:id>',views.profile_show,name='profile_show')
]