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
    path('add_dep', views.add_dep, name="add_dep"),
    path('unite_list', views.unite_list, name="unite_list"),
    path('dep_list', views.dep_list, name="dep_list"),
    path('update_unite/<pk>', views.UniteUpdateView.as_view() ),
    path('update_dep/<pk>', views.DepartementUpdateView.as_view() ),
    path('delete_unite/<int:id>', views.delete_unite, name="delete_unite"),
    path('delete_dep/<int:id>', views.delete_dep, name="delete_dep"),


    #comptes scf ---------------------------------------------
    # ajouter 
    path('scf/add_pos1', views.add_pos1, name="add_pos1"),
    path('scf/add_pos2', views.add_pos2, name="add_pos2"),
    path('scf/add_pos3', views.add_pos3, name="add_pos3"),
    path('scf/add_pos6', views.add_pos6, name="add_pos6"),
    path('scf/add_pos7', views.add_pos7, name="add_pos7"),
    path('scf/add_comptes', views.add_comptes, name="add_comptes"),
    # affichier
    path('scf/comptes_list', views.comptes_list, name="comptes_list"),
    # supprimer
    path('delete_pos1/<int:id>', views.delete_pos1, name="delete_pos1"),
    path('delete_pos2/<int:id>', views.delete_pos2, name="delete_pos2"),
    path('delete_pos3/<int:id>', views.delete_pos3, name="delete_pos3"),
    path('delete_pos6/<int:id>', views.delete_pos6, name="delete_pos6"),
    path('delete_pos7/<int:id>', views.delete_pos7, name="delete_pos7"),


    #others -------------------------------------------------------
    #monnaie
    path('ref/add_monnaie', views.add_monnaie, name="add_monnaie"),
    path('ref/monnaie_list', views.monnaie_list, name="monnaie_list"),
    path('ref/update_monnaie/<pk>', views.MonnaieUpdateView.as_view()),
    path('ref/delete_monnaie/<int:id>', views.delete_monnaie, name="delete_monnaie"),
    #taux de change
    path('ref/add_taux_chng', views.add_taux_chng, name="add_taux_chng"),
    path('ref/taux_chng_list', views.taux_chng_list, name="taux_chng_list"),
    path('ref/update_taux_chng/<pk>', views.TauxUpdateView.as_view()),
    path('ref/delete_taux_chng/<int:id>', views.delete_taux_chng, name="delete_taux_chng"),
    #chapitre
    path('ref/add_chapitre', views.add_chapitre, name="add_chapitre"),
    path('ref/chapitre_list', views.chapitre_list, name="chapitre_list"),
    path('ref/update_chapitre/<pk>', views.ChapitreUpdateView.as_view()),
    path('ref/delete_chapitre/<int:code_num>', views.delete_chapitre, name="delete_chapitre"),
    #pays
    path('ref/add_pays', views.add_pays, name="add_pays"),
    path('ref/pays_list', views.pays_list, name="pays_list"),
    path('ref/update_pays/<pk>', views.PaysUpdateView.as_view()),
    path('ref/delete_pays/<int:id>', views.delete_pays, name="delete_pays"),

   


]