from django.urls import path
from main import views

urlpatterns = [
    path('',views.home,name='home'), 
    path('ajouter_cadre', views.ajouter_cadre, name="ajouter_cadre"),
    path('ajouter_chef_dep', views.ajouter_chef_dep, name="ajouter_chef_dep"),
    path('ajouter_sous_dir', views.ajouter_sous_dir, name="ajouter_sous_dir"),
    path('ajouter_content_admin', views.ajouter_content_admin, name="ajouter_content_admin"),

    path('cadres_list', views.cadres_list, name="cadres_list"),
    path('chef_dep_list', views.chef_dep_list, name="chef_dep_list"),
    path('sous_dir_list', views.sous_dir_list, name="sous_dir_list"),
    path('content_admin_list', views.content_admin_list, name="content_admin_list"),

    path('delete_user/<int:id>', views.delete_user, name="delete_user"),


]