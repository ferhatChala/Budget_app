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
    path('ajouter_dir', views.ajouter_dir, name="ajouter_dir"),

    #afficher 
    path('cadres_list', views.cadres_list, name="cadres_list"),
    path('chef_dep_list', views.chef_dep_list, name="chef_dep_list"),
    path('sous_dir_list', views.sous_dir_list, name="sous_dir_list"),
    path('dir_list', views.dir_list, name="dir_list"),
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
    # affichier
    path('scf/comptes_list', views.comptes_list, name="comptes_list"),
    # supprimer
    path('delete_pos1/<int:id>', views.delete_pos1, name="delete_pos1"),
    path('delete_pos2/<int:id>', views.delete_pos2, name="delete_pos2"),
    path('delete_pos3/<int:id>', views.delete_pos3, name="delete_pos3"),
    path('delete_pos6/<int:id>', views.delete_pos6, name="delete_pos6"),
    path('delete_pos7/<int:id>', views.delete_pos7, name="delete_pos7"),
    #version 2
    path('add_compte', views.add_compte, name="add_compte"),
    path('scf_comptes', views.scf_comptes, name="scf_comptes"),


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

    # affectation des unites aux cadres 
    path('aff/show_cadres', views.show_cadres, name="show_cadres"),
    path('aff/show_unites/<int:id>', views.show_unites, name="show_unites"),
    path('aff/show_unites/add_unite_to_cadre/<int:id>', views.add_unite_to_cadre, name="add_unite_to_cadre"),
    path('aff/delete_unite_of_cadre/<int:id>', views.delete_unite_of_cadre, name="delete_unite_of_cadre"),
    
    # affectation des unites aux cadres 
    path('all_unites', views.all_unites, name="all_unites"),
    path('show_comptes/<int:id>', views.show_comptes, name="show_comptes"),
    path('show_comptes/add_compte_to_unite/<int:id>', views.add_compte_to_unite, name="add_compte_to_unite"),

    # proposition budget
    path('proposition/unites', views.unites, name="unites"),
    path('proposition/unite/<int:id>', views.unite_detail, name="unite"),

    path('proposition/unite/offre/<int:id>', views.offre_comptes, name="offre"),
    path('proposition/unite/traffic/<int:id>', views.traffic_comptes, name="traffic"),
    path('proposition/unite/ca_emmission/<int:id>', views.ca_emmission_comptes, name="ca_emmission"),
    path('proposition/unite/ca_transport/<int:id>', views.ca_transport_comptes, name="ca_transport"),
    path('proposition/unite/recettes/<int:id>', views.recettes_comptes, name="recettes"),
    path('proposition/unite/depense_fonc/<int:id>', views.depense_fonc_comptes, name="depense_fonc"),
    path('proposition/unite/depense_exp/<int:id>', views.depense_exp_comptes, name="depense_exp"),

    path('proposition/unite/offre/add_montant_offre/<int:id>', views.add_montant, name="add_montant_offre"),
    path('proposition/unite/traffic/add_montant_traffic/<int:id>', views.add_montant, name="add_montant_traffic"),
    path('proposition/unite/ca_emmission/add_montant_ca_emmission/<int:id>', views.add_montant, name="add_montant_ca_emmission"),
    path('proposition/unite/ca_transport/add_montant_ca_transport/<int:id>', views.add_montant, name="add_montant_ca_transport"),
    path('proposition/unite/recettes/add_montant_recettes/<int:id>', views.add_montant, name="add_montant_recettes"),
    path('proposition/unite/depense_fonc/add_montant_depense_fonc/<int:id>', views.add_montant, name="add_montant_depense_fonc"),
    path('proposition/unite/depense_exp/add_montant_depense_exp/<int:id>', views.add_montant, name="add_montant_depense_exp"),
    




   


]