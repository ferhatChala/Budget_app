from django.urls import path
from main import views

urlpatterns = [
    path('',views.home,name='home'), 
# Administration     
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
    path('interims', views.interims, name="interims"),
    path('interim/add', views.add_interim, name="add_interim"),
    #delete 
    path('delete_user/<int:id>', views.delete_user, name="delete_user"),
    path('update_user/<pk>', views.UserUpdateView.as_view() ),

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
    # annee budgétaire
    path('annee_bdg/add', views.add_annee_bdg, name="add_annee_bdg"),
    path('annee_bdg', views.annee_bdg, name="annee_bdg"),
    path('update_annee_bdg/<int:id>', views.update_annee_bdg, name="update_annee_bdg"),
    path('delete_annee_bdg/<int:id>', views.delete_annee_bdg, name="delete_annee_bdg"),



    # affectation des unites aux cadres 
    path('aff/show_cadres', views.show_cadres, name="show_cadres"),
    path('aff/show_unites/<int:id>', views.show_unites, name="show_unites"),
    path('aff/show_unites/add_unite_to_cadre/<int:id>', views.add_unite_to_cadre, name="add_unite_to_cadre"),
    path('aff/show_unites/delete_unite_of_cadre/<int:id>', views.delete_unite_of_cadre, name="delete_unite_of_cadre"),
    
    # affectation des comptes aux unites 
    path('all_unites', views.all_unites, name="all_unites"),
    path('show_comptes/<int:id>', views.show_comptes, name="show_comptes"),
    path('show_comptes/add_compte_to_unite/<int:id>', views.add_compte_to_unite, name="add_compte_to_unite"),
    path('show_comptes/delete_compte_of_unite/<int:id>', views.delete_compte_of_unite, name="delete_compte_of_unite"),

# proposition budget ----------------------------------------------------------------------------------------------------------
    path('proposition/unites', views.unites, name="unites"),
    path('proposition/unite/<int:id>', views.unite_detail, name="unite"),


    #Offre
    path('proposition/unite/offre/<int:id>', views.offre_comptes, name="offre"),
    path('proposition/unite/offre/add_montant_offre/<int:id>', views.add_montant, name="add_montant_offre"),
    path('proposition/unite/offre/update_montant/<int:id>', views.update_montant, name="update_montant" ),
    path('proposition/unite/offre/valid_montant/<int:id>', views.valid_montant, name="valid_montant" ),
    path('proposition/unite/offre/cancel_valid_montant/<int:id>', views.cancel_valid_montant, name="cancel_valid_montant" ),
    path('proposition/unite/offre/add_new_compte/<int:id>', views.add_new_compte, name="add_new_compte" ),
    path('proposition/unite/offre/delete_added_compte/<int:id>', views.delete_added_compte, name="delete_added_compte" ),
    path('proposition/unite/offre/update_comment/<int:id>', views.update_comment, name="update_comment"),
    path('proposition/unite/offre/delete_comment/<int:id>', views.delete_comment, name="delete_comment"),
    #Traffic
    path('proposition/unite/traffic/<int:id>', views.traffic_comptes, name="traffic"),
    path('proposition/unite/traffic/add_montant_traffic/<int:id>', views.add_montant, name="add_montant_traffic"),
    path('proposition/unite/traffic/update_montant/<int:id>', views.update_montant, name="update_montant" ),
    path('proposition/unite/traffic/valid_montant/<int:id>', views.valid_montant, name="valid_montant" ),
    path('proposition/unite/traffic/cancel_valid_montant/<int:id>', views.cancel_valid_montant, name="cancel_valid_montant" ),
    path('proposition/unite/traffic/add_new_compte/<int:id>', views.add_new_compte, name="add_new_compte" ),
    path('proposition/unite/traffic/delete_added_compte/<int:id>', views.delete_added_compte, name="delete_added_compte" ),
    path('proposition/unite/traffic/update_comment/<int:id>', views.update_comment, name="update_comment"),
    path('proposition/unite/traffic/delete_comment/<int:id>', views.delete_comment, name="delete_comment"),
    #ca emmission
    path('proposition/unite/ca_emmission/<int:id>', views.ca_emmission_comptes, name="ca_emmission"),
    path('proposition/unite/ca_emmission/add_montant_ca_emmission/<int:id>', views.add_montant, name="add_montant_ca_emmission"),
    path('proposition/unite/ca_emmission/update_montant/<int:id>', views.update_montant, name="update_montant" ),
    path('proposition/unite/ca_emmission/valid_montant/<int:id>', views.valid_montant, name="valid_montant" ),
    path('proposition/unite/ca_emmission/cancel_valid_montant/<int:id>', views.cancel_valid_montant, name="cancel_valid_montant" ),
    path('proposition/unite/ca_emmission/add_new_compte/<int:id>', views.add_new_compte, name="add_new_compte" ),
    path('proposition/unite/ca_emmission/delete_added_compte/<int:id>', views.delete_added_compte, name="delete_added_compte" ),
    path('proposition/unite/ca_emmission/update_comment/<int:id>', views.update_comment, name="update_comment"),
    path('proposition/unite/ca_emmission/delete_comment/<int:id>', views.delete_comment, name="delete_comment"),
    #ca transport
    path('proposition/unite/ca_transport/<int:id>', views.ca_transport_comptes, name="ca_transport"),
    path('proposition/unite/ca_transport/add_montant_ca_transport/<int:id>', views.add_montant, name="add_montant_ca_transport"),
    path('proposition/unite/ca_transport/update_montant/<int:id>', views.update_montant, name="update_montant" ),
    path('proposition/unite/ca_transport/valid_montant/<int:id>', views.valid_montant, name="valid_montant" ),
    path('proposition/unite/ca_transport/cancel_valid_montant/<int:id>', views.cancel_valid_montant, name="cancel_valid_montant" ),
    path('proposition/unite/ca_transport/add_new_compte/<int:id>', views.add_new_compte, name="add_new_compte" ),
    path('proposition/unite/ca_transport/delete_added_compte/<int:id>', views.delete_added_compte, name="delete_added_compte" ),
    path('proposition/unite/ca_transport/update_comment/<int:id>', views.update_comment, name="update_comment"),
    path('proposition/unite/ca_transport/delete_comment/<int:id>', views.delete_comment, name="delete_comment"),
    #autre reccettes
    path('proposition/unite/recettes/<int:id>', views.recettes_comptes, name="recettes"),
    path('proposition/unite/recettes/add_montant_recettes/<int:id>', views.add_montant, name="add_montant_recettes"),
    path('proposition/unite/recettes/update_montant/<int:id>', views.update_montant, name="update_montant" ),
    path('proposition/unite/recettes/valid_montant/<int:id>', views.valid_montant, name="valid_montant" ),
    path('proposition/unite/recettes/cancel_valid_montant/<int:id>', views.cancel_valid_montant, name="cancel_valid_montant" ),
    path('proposition/unite/recettes/add_new_compte/<int:id>', views.add_new_compte, name="add_new_compte" ),
    path('proposition/unite/recettes/delete_added_compte/<int:id>', views.delete_added_compte, name="delete_added_compte" ),
    path('proposition/unite/recettes/update_comment/<int:id>', views.update_comment, name="update_comment"),
    path('proposition/unite/recettes/delete_comment/<int:id>', views.delete_comment, name="delete_comment"),
    #depense foncionement
    path('proposition/unite/depense_fonc/<int:id>', views.depense_fonc_comptes, name="depense_fonc"),
    path('proposition/unite/depense_fonc/add_montant_depense_fonc/<int:id>', views.add_montant, name="add_montant_depense_fonc"),
    path('proposition/unite/depense_fonc/update_montant/<int:id>', views.update_montant, name="update_montant" ),
    path('proposition/unite/depense_fonc/valid_montant/<int:id>', views.valid_montant, name="valid_montant" ),
    path('proposition/unite/depense_fonc/cancel_valid_montant/<int:id>', views.cancel_valid_montant, name="cancel_valid_montant" ),
    path('proposition/unite/depense_fonc/add_new_compte/<int:id>', views.add_new_compte, name="add_new_compte" ),
    path('proposition/unite/depense_fonc/delete_added_compte/<int:id>', views.delete_added_compte, name="delete_added_compte" ),
    path('proposition/unite/depense_fonc/update_comment/<int:id>', views.update_comment, name="update_comment"),
    path('proposition/unite/depense_fonc/delete_comment/<int:id>', views.delete_comment, name="delete_comment"),
    #depense exploitation
    path('proposition/unite/depense_exp/<int:id>', views.depense_exp_comptes, name="depense_exp"),
    path('proposition/unite/depense_exp/add_montant_depense_exp/<int:id>', views.add_montant, name="add_montant_depense_exp"),
    path('proposition/unite/depense_exp/update_montant/<int:id>', views.update_montant, name="update_montant" ),
    path('proposition/unite/depense_exp/valid_montant/<int:id>', views.valid_montant, name="valid_montant" ),
    path('proposition/unite/depense_exp/cancel_valid_montant/<int:id>', views.cancel_valid_montant, name="cancel_valid_montant" ),
    path('proposition/unite/depense_exp/add_new_compte/<int:id>', views.add_new_compte, name="add_new_compte" ),
    path('proposition/unite/depense_exp/delete_added_compte/<int:id>', views.delete_added_compte, name="delete_added_compte" ),
    path('proposition/unite/depense_exp/update_comment/<int:id>', views.update_comment, name="update_comment"),
    path('proposition/unite/depense_exp/delete_comment/<int:id>', views.delete_comment, name="delete_comment"),
    # consultation bdg 
    path('proposition/annees', views.annees_bdg_prop, name="annees"),
    
    #--------------------------------------------------------------------------------------------------------------------------------

# Reunion budget ----------------------------------------------------------------------------------------------------------
    path('reunion/unites', views.unites_reunion, name="unites_reunion"),
    path('reunion/unite/<int:id>', views.unite_detail_reunion, name="unite_reunion"),

    #Offre
    path('reunion/unite/offre/<int:id>', views.offre_comptes_reunion, name="offre_reunion"),
    path('reunion/unite/offre/add_montant_offre/<int:id>', views.add_montant_reunion, name="add_montant_offre_reunion"),
    path('reunion/unite/offre/update_montant/<int:id>', views.update_montant_reunion, name="update_montant_reunion" ),
    path('reunion/unite/offre/valid_montant/<int:id>', views.valid_montant_reunion, name="valid_montant_reunion" ),
    path('reunion/unite/offre/valid_tous/<int:id_unite>/<int:ch_num>', views.valid_tous_reunion, name="valid_tous_reunion" ),
    path('reunion/unite/offre/cancel_valid_tous/<int:id_unite>/<int:ch_num>', views.cancel_valid_tous_reunion, name="cancel_valid_tous_reunion" ),
    path('reunion/unite/offre/cancel_valid_montant/<int:id>', views.cancel_valid_montant_reunion, name="cancel_valid_montant_reunion" ),
    path('reunion/unite/offre/add_new_compte/<int:id>', views.add_new_compte_reunion, name="add_new_compte_reunion" ),
    path('reunion/unite/offre/delete_added_compte/<int:id>', views.delete_added_compte_reunion, name="delete_added_compte_reunion" ),
    path('reunion/unite/offre/update_comment/<int:id>', views.update_comment_reunion, name="update_comment_reunion"),
    path('reunion/unite/offre/delete_comment/<int:id>', views.delete_comment_reunion, name="delete_comment_reunion"),
    #Traffic
    path('reunion/unite/traffic/<int:id>', views.traffic_comptes_reunion, name="traffic_reunion"),
    path('reunion/unite/traffic/add_montant_traffic/<int:id>', views.add_montant_reunion, name="add_montant_traffic_reunion"),
    path('reunion/unite/traffic/update_montant/<int:id>', views.update_montant_reunion, name="update_montant_reunion" ),
    path('reunion/unite/traffic/valid_montant/<int:id>', views.valid_montant_reunion, name="valid_montant_reunion" ),
    path('reunion/unite/traffic/cancel_valid_montant/<int:id>', views.cancel_valid_montant_reunion, name="cancel_valid_montant_reunion" ),
    path('reunion/unite/traffic/valid_tous/<int:id_unite>/<int:ch_num>', views.valid_tous_reunion, name="valid_tous_reunion" ),
    path('reunion/unite/traffic/cancel_valid_tous/<int:id_unite>/<int:ch_num>', views.cancel_valid_tous_reunion, name="cancel_valid_tous_reunion" ),    
   
    path('reunion/unite/traffic/add_new_compte/<int:id>', views.add_new_compte_reunion, name="add_new_compte_reunion" ),
    path('reunion/unite/traffic/delete_added_compte/<int:id>', views.delete_added_compte_reunion, name="delete_added_compte_reunion" ),
    path('reunion/unite/traffic/update_comment/<int:id>', views.update_comment_reunion, name="update_comment_reunion"),
    path('reunion/unite/traffic/delete_comment/<int:id>', views.delete_comment_reunion, name="delete_comment_reunion"),
    #ca emmission
    path('reunion/unite/ca_emmission/<int:id>', views.ca_emmission_comptes_reunion, name="ca_emmission_reunion"),
    path('reunion/unite/ca_emmission/add_montant_ca_emmission/<int:id>', views.add_montant_reunion, name="add_montant_ca_emmission_reunion"),
    path('reunion/unite/ca_emmission/update_montant/<int:id>', views.update_montant_reunion, name="update_montant_reunion" ),
    path('reunion/unite/ca_emmission/valid_montant/<int:id>', views.valid_montant_reunion, name="valid_montant_reunion" ),
    path('reunion/unite/ca_emmission/cancel_valid_montant/<int:id>', views.cancel_valid_montant_reunion, name="cancel_valid_montant_reunion" ),
    path('reunion/unite/ca_emmission/valid_tous/<int:id_unite>/<int:ch_num>', views.valid_tous_reunion, name="valid_tous_reunion" ),
    path('reunion/unite/ca_emmission/cancel_valid_tous/<int:id_unite>/<int:ch_num>', views.cancel_valid_tous_reunion, name="cancel_valid_tous_reunion" ),
    
    path('reunion/unite/ca_emmission/add_new_compte/<int:id>', views.add_new_compte_reunion, name="add_new_compte_reunion" ),
    path('reunion/unite/ca_emmission/delete_added_compte/<int:id>', views.delete_added_compte_reunion, name="delete_added_compte_reunion" ),
    path('reunion/unite/ca_emmission/update_comment/<int:id>', views.update_comment_reunion, name="update_comment_reunion"),
    path('reunion/unite/ca_emmission/delete_comment/<int:id>', views.delete_comment_reunion, name="delete_comment_reunion"),
    #ca transport
    path('reunion/unite/ca_transport/<int:id>', views.ca_transport_comptes_reunion, name="ca_transport_reunion"),
    path('reunion/unite/ca_transport/add_montant_ca_transport/<int:id>', views.add_montant_reunion, name="add_montant_ca_transport_reunion"),
    path('reunion/unite/ca_transport/update_montant/<int:id>', views.update_montant_reunion, name="update_montant_reunion" ),
    path('reunion/unite/ca_transport/valid_montant/<int:id>', views.valid_montant_reunion, name="valid_montant_reunion" ),
    path('reunion/unite/ca_transport/cancel_valid_montant/<int:id>', views.cancel_valid_montant_reunion, name="cancel_valid_montant_reunion" ),
    path('reunion/unite/ca_transport/valid_tous/<int:id_unite>/<int:ch_num>', views.valid_tous_reunion, name="valid_tous_reunion" ),
    path('reunion/unite/ca_transport/cancel_valid_tous/<int:id_unite>/<int:ch_num>', views.cancel_valid_tous_reunion, name="cancel_valid_tous_reunion" ),
   
    path('reunion/unite/ca_transport/add_new_compte/<int:id>', views.add_new_compte_reunion, name="add_new_compte_reunion" ),
    path('reunion/unite/ca_transport/delete_added_compte/<int:id>', views.delete_added_compte_reunion, name="delete_added_compte_reunion" ),
    path('reunion/unite/ca_transport/update_comment/<int:id>', views.update_comment_reunion, name="update_comment_reunion"),
    path('reunion/unite/ca_transport/delete_comment/<int:id>', views.delete_comment_reunion, name="delete_comment_reunion"),
    #autre reccettes
    path('reunion/unite/recettes/<int:id>', views.recettes_comptes_reunion, name="recettes_reunion"),
    path('reunion/unite/recettes/add_montant_recettes/<int:id>', views.add_montant_reunion, name="add_montant_recettes_reunion"),
    path('reunion/unite/recettes/update_montant/<int:id>', views.update_montant_reunion, name="update_montant_reunion" ),
    path('reunion/unite/recettes/valid_montant/<int:id>', views.valid_montant_reunion, name="valid_montant_reunion" ),
    path('reunion/unite/recettes/cancel_valid_montant/<int:id>', views.cancel_valid_montant_reunion, name="cancel_valid_montant_reunion" ),
    path('reunion/unite/recettes/valid_tous/<int:id_unite>/<int:ch_num>', views.valid_tous_reunion, name="valid_tous_reunion" ),
    path('reunion/unite/recettes/cancel_valid_tous/<int:id_unite>/<int:ch_num>', views.cancel_valid_tous_reunion, name="cancel_valid_tous_reunion" ),
   
    path('reunion/unite/recettes/add_new_compte/<int:id>', views.add_new_compte_reunion, name="add_new_compte_reunion" ),
    path('reunion/unite/recettes/delete_added_compte/<int:id>', views.delete_added_compte_reunion, name="delete_added_compte_reunion" ),
    path('reunion/unite/recettes/update_comment/<int:id>', views.update_comment_reunion, name="update_comment_reunion"),
    path('reunion/unite/recettes/delete_comment/<int:id>', views.delete_comment_reunion, name="delete_comment_reunion"),
    #depense foncionement
    path('reunion/unite/depense_fonc/<int:id>', views.depense_fonc_comptes_reunion, name="depense_fonc_reunion"),
    path('reunion/unite/depense_fonc/add_montant_depense_fonc/<int:id>', views.add_montant_reunion, name="add_montant_depense_fonc_reunion"),
    path('reunion/unite/depense_fonc/update_montant/<int:id>', views.update_montant_reunion, name="update_montant_reunion" ),
    path('reunion/unite/depense_fonc/valid_montant/<int:id>', views.valid_montant_reunion, name="valid_montant_reunion" ),
    path('reunion/unite/depense_fonc/cancel_valid_montant/<int:id>', views.cancel_valid_montant_reunion, name="cancel_valid_montant_reunion" ),
    path('reunion/unite/depense_fonc/valid_tous/<int:id_unite>/<int:ch_num>', views.valid_tous_reunion, name="valid_tous_reunion" ),
    path('reunion/unite/depense_fonc/cancel_valid_tous/<int:id_unite>/<int:ch_num>', views.cancel_valid_tous_reunion, name="cancel_valid_tous_reunion" ),
   
    path('reunion/unite/depense_fonc/add_new_compte/<int:id>', views.add_new_compte_reunion, name="add_new_compte_reunion" ),
    path('reunion/unite/depense_fonc/delete_added_compte/<int:id>', views.delete_added_compte_reunion, name="delete_added_compte_reunion" ),
    path('reunion/unite/depense_fonc/update_comment/<int:id>', views.update_comment_reunion, name="update_comment_reunion"),
    path('reunion/unite/depense_fonc/delete_comment/<int:id>', views.delete_comment_reunion, name="delete_comment_reunion"),
    #depense exploitation
    path('reunion/unite/depense_exp/<int:id>', views.depense_exp_comptes_reunion, name="depense_exp_reunion"),
    path('reunion/unite/depense_exp/add_montant_depense_exp/<int:id>', views.add_montant_reunion, name="add_montant_depense_exp_reunion"),
    path('reunion/unite/depense_exp/update_montant/<int:id>', views.update_montant_reunion, name="update_montant_reunion" ),
    path('reunion/unite/depense_exp/valid_montant/<int:id>', views.valid_montant_reunion, name="valid_montant_reunion" ),
    path('reunion/unite/depense_exp/cancel_valid_montant/<int:id>', views.cancel_valid_montant_reunion, name="cancel_valid_montant_reunion" ),
    path('reunion/unite/depense_exp/valid_tous/<int:id_unite>/<int:ch_num>', views.valid_tous_reunion, name="valid_tous_reunion" ),
    path('reunion/unite/depense_exp/cancel_valid_tous/<int:id_unite>/<int:ch_num>', views.cancel_valid_tous_reunion, name="cancel_valid_tous_reunion" ),
    
    path('reunion/unite/depense_exp/add_new_compte/<int:id>', views.add_new_compte_reunion, name="add_new_compte_reunion" ),
    path('reunion/unite/depense_exp/delete_added_compte/<int:id>', views.delete_added_compte_reunion, name="delete_added_compte_reunion" ),
    path('reunion/unite/depense_exp/update_comment/<int:id>', views.update_comment_reunion, name="update_comment_reunion"),
    path('reunion/unite/depense_exp/delete_comment/<int:id>', views.delete_comment_reunion, name="delete_comment_reunion"),
    # consultation bdg 
    path('reunion/annees', views.annees_bdg_reunion, name="annees_reunion"),
    
    #--------------------------------------------------------------------------------------------------------------------------------


    #----------------------------------------------------------------------------------------------------------

# Notification budget budget ----------------------------------------------------------------------------------------------------------
    path('notif/unites', views.unites_notif, name="unites_notif"),
    path('notif/unite/<int:id>', views.unite_detail_notif, name="unite_notif"),

    #Offre
    path('notif/unite/offre/<int:id>', views.offre_comptes_notif, name="offre_notif"),
    path('notif/unite/offre/add_montant/<int:id>', views.add_montant_notif, name="add_montant_offre_notif"),
    path('notif/unite/offre/update_montant/<int:id>', views.update_montant_notif, name="update_montant_notif" ),
    path('notif/unite/offre/valid_montant/<int:id>', views.valid_montant_notif, name="valid_montant_notif" ),
    path('notif/unite/offre/valid_tous/<int:id_unite>/<int:ch_num>', views.valid_tous_notif, name="valid_tous_notif" ),
    path('notif/unite/offre/cancel_valid_tous/<int:id_unite>/<int:ch_num>', views.cancel_valid_tous_notif, name="cancel_valid_tous_notif" ),
    path('notif/unite/offre/cancel_valid_montant/<int:id>', views.cancel_valid_montant_notif, name="cancel_valid_montant_notif" ),
    path('notif/unite/offre/add_new_compte/<int:id>', views.add_new_compte_notif, name="add_new_compte_notif" ),
    path('notif/unite/offre/delete_added_compte/<int:id>', views.delete_added_compte_notif, name="delete_added_compte_notif" ),
    path('notif/unite/offre/update_comment/<int:id>', views.update_comment_notif, name="update_comment_notif"),
    path('notif/unite/offre/delete_comment/<int:id>', views.delete_comment_notif, name="delete_comment_notif"),
    #Traffic
    path('notif/unite/traffic/<int:id>', views.traffic_comptes_notif, name="traffic_notif"),
    path('notif/unite/traffic/add_montant/<int:id>', views.add_montant_notif, name="add_montant_traffic_notif"),
    path('notif/unite/traffic/update_montant/<int:id>', views.update_montant_notif, name="update_montant_notif" ),
    path('notif/unite/traffic/valid_montant/<int:id>', views.valid_montant_notif, name="valid_montant_notif" ),
    path('notif/unite/traffic/cancel_valid_montant/<int:id>', views.cancel_valid_montant_notif, name="cancel_valid_montant_notif" ),
    path('notif/unite/traffic/valid_tous/<int:id_unite>/<int:ch_num>', views.valid_tous_notif, name="valid_tous_notif" ),
    path('notif/unite/traffic/cancel_valid_tous/<int:id_unite>/<int:ch_num>', views.cancel_valid_tous_notif, name="cancel_valid_tous_notif" ),    
   
    path('notif/unite/traffic/add_new_compte/<int:id>', views.add_new_compte_notif, name="add_new_compte_notif" ),
    path('notif/unite/traffic/delete_added_compte/<int:id>', views.delete_added_compte_notif, name="delete_added_compte_notif" ),
    path('notif/unite/traffic/update_comment/<int:id>', views.update_comment_notif, name="update_comment_notif"),
    path('notif/unite/traffic/delete_comment/<int:id>', views.delete_comment_notif, name="delete_comment_notif"),
    #ca emmission
    path('notif/unite/ca_emmission/<int:id>', views.ca_emmission_comptes_notif, name="ca_emmission_notif"),
    path('notif/unite/ca_emmission/add_montant/<int:id>', views.add_montant_notif, name="add_montant_ca_emmission_notif"),
    path('notif/unite/ca_emmission/update_montant/<int:id>', views.update_montant_notif, name="update_montant_notif" ),
    path('notif/unite/ca_emmission/valid_montant/<int:id>', views.valid_montant_notif, name="valid_montant_notif" ),
    path('notif/unite/ca_emmission/cancel_valid_montant/<int:id>', views.cancel_valid_montant_notif, name="cancel_valid_montant_notif" ),
    path('notif/unite/ca_emmission/valid_tous/<int:id_unite>/<int:ch_num>', views.valid_tous_notif, name="valid_tous_notif" ),
    path('notif/unite/ca_emmission/cancel_valid_tous/<int:id_unite>/<int:ch_num>', views.cancel_valid_tous_notif, name="cancel_valid_tous_notif" ),
    
    path('notif/unite/ca_emmission/add_new_compte/<int:id>', views.add_new_compte_notif, name="add_new_compte_notif" ),
    path('notif/unite/ca_emmission/delete_added_compte/<int:id>', views.delete_added_compte_notif, name="delete_added_compte_notif" ),
    path('notif/unite/ca_emmission/update_comment/<int:id>', views.update_comment_notif, name="update_comment_notif"),
    path('notif/unite/ca_emmission/delete_comment/<int:id>', views.delete_comment_notif, name="delete_comment_notif"),
    #ca transport
    path('notif/unite/ca_transport/<int:id>', views.ca_transport_comptes_notif, name="ca_transport_notif"),
    path('notif/unite/ca_transport/add_montant/<int:id>', views.add_montant_notif, name="add_montant_ca_transport_notif"),
    path('notif/unite/ca_transport/update_montant/<int:id>', views.update_montant_notif, name="update_montant_notif" ),
    path('notif/unite/ca_transport/valid_montant/<int:id>', views.valid_montant_notif, name="valid_montant_notif" ),
    path('notif/unite/ca_transport/cancel_valid_montant/<int:id>', views.cancel_valid_montant_notif, name="cancel_valid_montant_notif" ),
    path('notif/unite/ca_transport/valid_tous/<int:id_unite>/<int:ch_num>', views.valid_tous_notif, name="valid_tous_notif" ),
    path('notif/unite/ca_transport/cancel_valid_tous/<int:id_unite>/<int:ch_num>', views.cancel_valid_tous_notif, name="cancel_valid_tous_notif" ),
   
    path('notif/unite/ca_transport/add_new_compte/<int:id>', views.add_new_compte_notif, name="add_new_compte_notif" ),
    path('notif/unite/ca_transport/delete_added_compte/<int:id>', views.delete_added_compte_notif, name="delete_added_compte_notif" ),
    path('notif/unite/ca_transport/update_comment/<int:id>', views.update_comment_notif, name="update_comment_notif"),
    path('notif/unite/ca_transport/delete_comment/<int:id>', views.delete_comment_notif, name="delete_comment_notif"),
    #autre reccettes
    path('notif/unite/recettes/<int:id>', views.recettes_comptes_notif, name="recettes_notif"),
    path('notif/unite/recettes/add_montant/<int:id>', views.add_montant_notif, name="add_montant_recettes_notif"),
    path('notif/unite/recettes/update_montant/<int:id>', views.update_montant_notif, name="update_montant_notif" ),
    path('notif/unite/recettes/valid_montant/<int:id>', views.valid_montant_notif, name="valid_montant_notif" ),
    path('notif/unite/recettes/cancel_valid_montant/<int:id>', views.cancel_valid_montant_notif, name="cancel_valid_montant_notif" ),
    path('notif/unite/recettes/valid_tous/<int:id_unite>/<int:ch_num>', views.valid_tous_notif, name="valid_tous_notif" ),
    path('notif/unite/recettes/cancel_valid_tous/<int:id_unite>/<int:ch_num>', views.cancel_valid_tous_notif, name="cancel_valid_tous_notif" ),
   
    path('notif/unite/recettes/add_new_compte/<int:id>', views.add_new_compte_notif, name="add_new_compte_notif" ),
    path('notif/unite/recettes/delete_added_compte/<int:id>', views.delete_added_compte_notif, name="delete_added_compte_notif" ),
    path('notif/unite/recettes/update_comment/<int:id>', views.update_comment_notif, name="update_comment_notif"),
    path('notif/unite/recettes/delete_comment/<int:id>', views.delete_comment_notif, name="delete_comment_notif"),
    #depense foncionement
    path('notif/unite/depense_fonc/<int:id>', views.depense_fonc_comptes_notif, name="depense_fonc_notif"),
    path('notif/unite/depense_fonc/add_montant/<int:id>', views.add_montant_notif, name="add_montant_depense_fonc_notif"),
    path('notif/unite/depense_fonc/update_montant/<int:id>', views.update_montant_notif, name="update_montant_notif" ),
    path('notif/unite/depense_fonc/valid_montant/<int:id>', views.valid_montant_notif, name="valid_montant_notif" ),
    path('notif/unite/depense_fonc/cancel_valid_montant/<int:id>', views.cancel_valid_montant_notif, name="cancel_valid_montant_notif" ),
    path('notif/unite/depense_fonc/valid_tous/<int:id_unite>/<int:ch_num>', views.valid_tous_notif, name="valid_tous_notif" ),
    path('notif/unite/depense_fonc/cancel_valid_tous/<int:id_unite>/<int:ch_num>', views.cancel_valid_tous_notif, name="cancel_valid_tous_notif" ),
   
    path('notif/unite/depense_fonc/add_new_compte/<int:id>', views.add_new_compte_notif, name="add_new_compte_notif" ),
    path('notif/unite/depense_fonc/delete_added_compte/<int:id>', views.delete_added_compte_notif, name="delete_added_compte_notif" ),
    path('notif/unite/depense_fonc/update_comment/<int:id>', views.update_comment_notif, name="update_comment_notif"),
    path('notif/unite/depense_fonc/delete_comment/<int:id>', views.delete_comment_notif, name="delete_comment_notif"),
    #depense exploitation
    path('notif/unite/depense_exp/<int:id>', views.depense_exp_comptes_notif, name="depense_exp_notif"),
    path('notif/unite/depense_exp/add_montant/<int:id>', views.add_montant_notif, name="add_montant_depense_exp_notif"),
    path('notif/unite/depense_exp/update_montant/<int:id>', views.update_montant_notif, name="update_montant_notif" ),
    path('notif/unite/depense_exp/valid_montant/<int:id>', views.valid_montant_notif, name="valid_montant_notif" ),
    path('notif/unite/depense_exp/cancel_valid_montant/<int:id>', views.cancel_valid_montant_notif, name="cancel_valid_montant_notif" ),
    path('notif/unite/depense_exp/valid_tous/<int:id_unite>/<int:ch_num>', views.valid_tous_notif, name="valid_tous_notif" ),
    path('notif/unite/depense_exp/cancel_valid_tous/<int:id_unite>/<int:ch_num>', views.cancel_valid_tous_notif, name="cancel_valid_tous_notif" ),
    
    path('notif/unite/depense_exp/add_new_compte/<int:id>', views.add_new_compte_notif, name="add_new_compte_notif" ),
    path('notif/unite/depense_exp/delete_added_compte/<int:id>', views.delete_added_compte_notif, name="delete_added_compte_notif" ),
    path('notif/unite/depense_exp/update_comment/<int:id>', views.update_comment_notif, name="update_comment_notif"),
    path('notif/unite/depense_exp/delete_comment/<int:id>', views.delete_comment_notif, name="delete_comment_notif"),
    # budget menseulle ---------------------
    path('notif_mens/unite/<int:id>', views.unite_detail_notif_m, name="unite_notif_m"),    
    #Offre
    path('notif_mens/unite/offre/<int:id>', views.offre_comptes_notif_m, name="offre_notif_m"),
    path('notif_mens/unite/offre/add_montant/<int:id>', views.add_montant_notif_m, name="add_montant_offre_notif_m"),
    path('notif_mens/unite/offre/update_montant/<int:id>', views.update_montant_notif_m, name="update_montant_notif_m" ),
    path('notif_mens/unite/offre/valid_montant/<int:id>', views.valid_montant_notif_m, name="valid_montant_notif_m" ),
    path('notif_mens/unite/offre/valid_tous/<int:id_unite>/<int:ch_num>', views.valid_tous_notif_m, name="valid_tous_notif_m" ),
    path('notif_mens/unite/offre/cancel_valid_tous/<int:id_unite>/<int:ch_num>', views.cancel_valid_tous_notif_m, name="cancel_valid_tous_notif_m" ),
    path('notif_mens/unite/offre/cancel_valid_montant/<int:id>', views.cancel_valid_montant_notif_m, name="cancel_valid_montant_notif_m" ),
    path('notif_mens/unite/offre/add_new_compte/<int:id>', views.add_new_compte_notif_m, name="add_new_compte_notif_m" ),
    path('notif_mens/unite/offre/delete_added_compte/<int:id>', views.delete_added_compte_notif_m, name="delete_added_compte_notif_m" ),
    path('notif_mens/unite/offre/update_comment/<int:id>', views.update_comment_notif_m, name="update_comment_notif_m"),
    path('notif_mens/unite/offre/delete_comment/<int:id>', views.delete_comment_notif_m, name="delete_comment_notifm"),
    
    # consultation bdg --------------------
    path('notif/annees', views.annees_bdg_notif, name="annees_notif"),
    
    #--------------------------------------------------------------------------------------------------------------------------------



]