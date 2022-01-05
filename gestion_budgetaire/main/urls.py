from django.urls import path
from main import views

urlpatterns = [
    path('',views.home,name='home'), 
    #users ---------------------------------------------------
    #ajouter 
    path('ajouter_cadre', views.ajouter_cadre, name="ajouter_cadre"),
    path('ajouter_chef_dep', views.ajouter_chef_dep, name="ajouter_chef_dep"),
    path('ajouter_sous_dir', views.ajouter_sous_dir, name="ajouter_sous_dir"),
    path('ajouter_content_admin', views.ajouter_content_admin, name="ajouter_content_admin"),
    #afficher 
    path('cadres_list', views.cadres_list, name="cadres_list"),
    path('chef_dep_list', views.chef_dep_list, name="chef_dep_list"),
    path('sous_dir_list', views.sous_dir_list, name="sous_dir_list"),
    path('content_admin_list', views.content_admin_list, name="content_admin_list"),
    #delete 
    path('delete_user/<int:id>', views.delete_user, name="delete_user"),

    #unités & departement-------------------------------------
    path('add_unite', views.add_unite, name="add_unite"),
    path('add_dep', views.ajouter_cadre, name="add_dep"),
    path('unite_list', views.unite_list, name="unite_list"),
    path('dep_list', views.dep_list, name="dep_list"),
    
    #comptes scf ---------------------------------------------
    # ajouter 
    path('scf/add_pos1', views.add_pos1, name="add_pos1"),
    path('scf/add_pos2', views.add_pos2, name="add_pos2"),
    path('scf/add_pos3', views.add_pos3, name="add_pos3"),
    path('scf/add_pos6', views.add_pos6, name="add_pos6"),
    path('scf/add_pos7', views.add_pos7, name="add_pos7"),
    # affichier
    path('scf/comptes_list', views.comptes_list, name="comptes_list"),
   








]