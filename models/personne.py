# -*- coding: utf-8 -*-

from odoo import api, fields, models

class CrmPerson(models.Model):
    _name = 'crm.lead'
    _inherit = 'crm.lead'

    marque_code = fields.Many2one(comodel_name="person.marque", string="Code marque", required=True, )
    marque_libelle = fields.Char(related="marque_code.libelle_marque", string="Libelle Marque", required=False, )
    source_code = fields.Many2one(comodel_name="person.source", string="Code source", required=True, )
    source_libelle = fields.Char(related="source_code.libelle_source", string="Libelle source", required=False, )
    id_cdp = fields.Char(compute='_compute_id', string="Identifiant", required=False, )

    id_personne_marque = fields.Selection(string="Identifiant Personne Marque", selection=[('ss', 'SS'), ('mobile', 'Mobile'), ('email', 'Email'), ], required=False, )
    type_id_marque = fields.Selection(string="ID Type Marque", selection=[('base_annonceur', 'base annonceur'), ('mobile', 'Mobile'), ('email', 'Email'),('erp', 'Erp'),('ss', 'SS'),('media', 'Media'), ], required=False, )
    type_personne = fields.Selection(string="Type personne",
                                     selection=[('PP', ' PERSPONNE PHYSIQUE'), ('PM', ' PERSONNE MORALE'), ],
                                     required=False, )
    statut_personne = fields.Selection(string="Statut",
                                       selection=[('00', 'PROSPECT'), ('01', 'CLIENT'), ('02', 'CANDIDAT'),
                                                  ('03', ' FRANCHISE POTENTIEL'), ], required=False, )
    libelle_statut_personne = fields.Char(string="Libelle statut", required=False, )
    role_personne = fields.Selection(string="", selection=[('reprentant PM', 'Reprentant PM'), ('aidant', 'Aidant'), ],
                                     required=False, )
    fonction_personne = fields.Char(string="Fonction", required=False, )
    origine_recrutement = fields.Many2one(comodel_name="origine.recrutement", string="Origine recrutement", required=False, )
    code_point_de_vente = fields.Char(string="Code point de vente", required=False, )
    libelle_point_de_vente = fields.Char(string="Libelle point de vente", required=False, )
    type_point_de_vente = fields.Selection(string="Type point de vente",
                                      selection=[('I', 'Intégré'), ('F', 'Franchisé'), ],
                                      required=False, )
    secteur_activite_societe = fields.Char(string="Secteur d'activité de socièté", required=False, )
    secteur_societe = fields.Char(string="Secteur de socièté", required=False, )
    date_naissance = fields.Date(string="Date de naissance", required=False, )
    acceptation_cgu = fields.Boolean(string="Acceptation CGU",)
    date_acceptation_cgu = fields.Datetime(string="Date d'acceptation CGU", required=False, )
    affectation = fields.Datetime(string="Date Affectation", required=False, )
    regime_matrimonial = fields.Char(string="Régime matrimonial", required=False, )
    composition_foyer = fields.Integer(string="Composition foyer", required=False, )
    date_naissance_conjoint = fields.Date(string="Date naissance conjoint", required=False, )
    date_naissance_enfant1 = fields.Date(string="Date naissance enfant 1", required=False, )
    date_naissance_enfant2 = fields.Date(string="Date naissance enfant 2", required=False, )
    date_naissance_enfant3 = fields.Date(string="Date naissance enfant 3", required=False, )
    interaction_ids = fields.One2many(comodel_name="person.interaction", inverse_name="lead_id", string="Intéractions", required=False, )

    statut_membre = fields.Char(string="Statut membre", required=False, )
    solde_compte_fidelite = fields.Float(string="Solde compte fidelité", required=False, selection=[('t', 'PA'),('E', 'Engagement'),('R', 'Relationnel'), ], )
    cumul_pa = fields.Float(string="",  required=False, )
    cumul_earn = fields.Float(string="",  required=False, )
    cumul_burn = fields.Float(string="",  required=False, )
    cumul_participations = fields.Float(string="",  required=False, )
    cumul_telechargement_coupon = fields.Float(string="",  required=False, )
    cumul_usage_coupon = fields.Float(string="",  required=False, )
    cumul_sollicitations = fields.Float(string="",  required=False, )
    cumul_interactions = fields.Float(string="",  required=False, )
    age = fields.Integer(string="Age", required=False, )

    @api.depends('marque_code.code_marque')
    def _compute_id(self):
        for record in self:
            record.id_cdp = record.id
            if record.marque_code.code_marque:
                record.id_cdp = record.marque_code.code_marque + str(record.id)

class Interaction(models.Model):
    _name = 'person.interaction'
    _rec_name = 'code_interaction'


    date_interaction = fields.Date(string="Date Intéraction", required=False, )
    interaction = fields.Many2one(comodel_name="interaction.interaction", string="Libellé Intéraction", required=True, )
    code_interaction = fields.Char(related="interaction.code_interaction", string="Code Intéraction", required=False, )
    type_interaction = fields.Char(compute="_get_type_interaction", string="Type Intéraction", required=False, )
    libelle_type_interaction = fields.Char(compute="_get_libelle_type_interaction", string="Libellé Type Intéraction", required=False, )
    valeur_interaction = fields.Selection(string="Valeur Intéraction", selection=[('0', 'Oui'), ('1', 'Non'),('9', 'Pas de réponse'), ], required=False, )
    lead_id = fields.Many2one(comodel_name="crm.lead", required=True, )
    id_code_person = fields.Char(related="lead_id.id_cdp", string="Identifiant Personne", required=False, )
    id_personne_marque = fields.Selection(related="lead_id.id_personne_marque", required=False, )
    marque_code = fields.Many2one(related="lead_id.marque_code", string="Code marque", required=False, )
    source_code = fields.Many2one(related="lead_id.source_code", string="Code source", required=False, )
    inter_cnstm = fields.One2many(comodel_name="interaction.consentement", inverse_name="pers_inter_cons", string="Consentements", required=False, )
    inter_abnms = fields.One2many(comodel_name="interaction.abonnement", inverse_name="pers_inter_abn", string="Abonnements", required=False, )
    inter_prtcps = fields.One2many(comodel_name="interaction.participation", inverse_name="pers_inter_particip", string="Participations", required=False, )
    inter_orders = fields.One2many(comodel_name="interaction.order", inverse_name="pers_inter_order", string="Commandes", required=False, )
    inter_coupons = fields.One2many(comodel_name="interaction.coupons", inverse_name="pers_inter_coupons", string="Coupons", required=False, )
    inter_sollicits = fields.One2many(comodel_name="interaction.sollicitation", inverse_name="pers_inter_sollic", string="Sollicitations", required=False, )
    inter_us_services = fields.One2many(comodel_name="interaction.usage.service", inverse_name="pers_inter_us_service", string="Usages des services", required=False, )
    inter_contacts = fields.One2many(comodel_name="interaction.contact", inverse_name="pers_inter_contact", string="Contacts", required=False, )
    inter_offres = fields.One2many(comodel_name="interaction.offre", inverse_name="pers_inter_offre", string="Offres", required=False, )
    inter_fidel_earns = fields.One2many(comodel_name="interaction.fidelite.earn", inverse_name="pers_inter_fidel", string="Fidelité Earn", required=False, )
    inter_fidel_burns = fields.One2many(comodel_name="interaction.fidelite.burn", inverse_name="pers_inter_fidel", string="Fidelité Burn", required=False, )


    @api.depends('interaction.libelle_interaction')
    def _get_type_interaction(self):
        for record in self:
            record.type_interaction = "code_"
            if record.interaction:
                record.type_interaction = "code_" + record.interaction.libelle_interaction

    @api.depends('interaction.libelle_interaction')
    def _get_libelle_type_interaction(self):
        for record in self:
            record.libelle_type_interaction = "libelle_"
            if record.interaction:
                record.libelle_type_interaction = "libelle_" + record.interaction.libelle_interaction


class Marque(models.Model):
    _name = 'person.marque'
    _rec_name = 'code_marque'

    code_marque = fields.Char(string="Code marque", required=True, )
    libelle_marque = fields.Char(string="Libellé marque", required=False, )

class Source(models.Model):
    _name = 'person.source'
    _rec_name = 'code_source'

    code_source = fields.Char(string="Code Source", required=True, )
    libelle_source = fields.Char(string="Libellé Source", required=False, )


class OrigineRecrutement(models.Model):
    _name = 'origine.recrutement'
    _rec_name = 'code_origine'

    code_origine = fields.Char(string="Code Origine", required=True, )
    libelle_origine = fields.Char(string="Libellé Origine", required=False, )

class LeadInteraction(models.Model):
    _name = 'interaction.interaction'
    _rec_name = 'libelle_interaction'

    code_interaction = fields.Char(string="Code Intéraction", required=True, )
    libelle_interaction = fields.Char(string="Libellé Intéraction", required=False, )

class Consentement(models.Model):
    _name = 'consentement.consentement'
    _rec_name = 'code_consentement'

    code_consentement = fields.Char(string="Code Consentement", required=True, )
    libelle_consentement = fields.Char(string="Libellé Consentement", required=False, )

class Abonnement(models.Model):
    _name = 'abonnement.abonnement'
    _rec_name = 'code_abonnement'

    code_abonnement = fields.Char(string="Code Abonnement", required=True, )
    libelle_abonnement = fields.Char(string="Libellé Abonnement", required=False, )

class Participation(models.Model):
    _name = 'participation.participation'
    _rec_name = 'code_participation'

    code_participation = fields.Char(string="Code Participation", required=True, )
    libelle_participation = fields.Char(string="Libellé Participation", required=False, )

class UsageService(models.Model):
    _name = 'usage.service'
    _rec_name = 'code_usage'

    code_usage = fields.Char(string="Code Usage", required=True, )
    libelle_usage = fields.Char(string="Libellé Usage", required=False, )

class Contacts(models.Model):
    _name = 'contact.contact'
    _rec_name = 'code_contact'

    code_contact = fields.Char(string="Code Contact", required=True, )
    libelle_contact = fields.Char(string="Libellé Contact", required=False, )


class Offres(models.Model):
    _name = 'offre.offre'
    _rec_name = 'code_offre'

    code_offre = fields.Char(string="Code Offre", required=True, )
    libelle_offre = fields.Char(string="Libellé Offre", required=False, )

class InteractionConsentement(models.Model):
    _name = 'interaction.consentement'
    _rec_name = 'pers_inter_cons'

    date_cnstm = fields.Date(string="Date Consentement", required=False, )
    code_cnstm = fields.Many2one(comodel_name="consentement.consentement",string="Code Consentement", required=True, )
    libelle_cnstm = fields.Char(related="code_cnstm.libelle_consentement", string="Libellé Consentement", )
    support_cnstm = fields.Selection(string="Support Consentement", selection=[('mail', 'e-mail'),('mob', 'mobile'), ('tel', 'téléphone'), ], required=False, )
    valeur_cnstm = fields.Selection(string="Valeur Consentement", selection=[('0', 'OPT-IN NON'), ('1', 'OPT-IN OUI'),('9', 'OUTPUT'), ], required=False, )
    pers_inter_cons = fields.Many2one(comodel_name="person.interaction", string="Code Intéraction", required=False, )
    id_interaction = fields.Integer(related="pers_inter_cons.id", string="Identifiant Intéraction", required=False, )
    id_pers_cdp = fields.Char(related="pers_inter_cons.id_code_person", string="Identifiant Personne", required=False, )
    id_pers_marq = fields.Selection(related="pers_inter_cons.id_personne_marque", string="Identifiant Personne Marque", required=False, )
    id_cd_marq = fields.Many2one(related="pers_inter_cons.marque_code", string="Personne Marque", required=False, )
    id_cd_src = fields.Many2one(related="pers_inter_cons.source_code", string="Personne Source", required=False, )


class InteractionAbonnement(models.Model):
    _name = 'interaction.abonnement'
    _rec_name = 'pers_inter_abn'

    date_abn = fields.Datetime(string="Date Abonnement", required=False, )
    code_abn = fields.Many2one(comodel_name="abonnement.abonnement",string="Code Abonnement", required=True, )
    libelle_abn = fields.Char(related="code_abn.libelle_abonnement", string="Libellé Abonnement", )
    cordonnee_abn = fields.Selection(string="Cordonnées Abonnement", selection=[('mail', 'e-mail'),('mob', 'mobile'), ('tel', 'téléphone'), ], required=False, )
    valeur_abn = fields.Selection(string="Valeur Consentement", selection=[('0', 'NON'), ('1', 'OUI'),], required=False, )
    pers_inter_abn = fields.Many2one(comodel_name="person.interaction", string="Code Intéraction", required=False, )
    id_interaction_abn = fields.Integer(related="pers_inter_abn.id", string="Identifiant Intéraction", required=False, )
    id_pers_cdp_abn = fields.Char(related="pers_inter_abn.id_code_person", string="Identifiant Personne", required=False, )
    id_pers_marq_abn = fields.Selection(related="pers_inter_abn.id_personne_marque", string="Identifiant Personne Marque", required=False, )
    id_cd_marq_abn = fields.Many2one(related="pers_inter_abn.marque_code", string="Personne Marque", required=False, )
    id_cd_src_abn = fields.Many2one(related="pers_inter_abn.source_code", string="Personne Source", required=False, )

class InteractionParticipation(models.Model):
    _name = 'interaction.participation'
    _rec_name = 'pers_inter_particip'

    date_participation = fields.Datetime(string="Date Participation", required=False, )
    code_operation = fields.Many2one(comodel_name="participation.participation",string="Code Opération", required=True, )
    libelle_operation = fields.Char(related="code_operation.libelle_participation", string="Libellé Opération", )
    type_operation = fields.Selection(string="Type Opération", selection=[('jeux,', 'jeux'),('concours,', 'concours'), ('activation', 'activation'), ], required=False, )
    res_participation = fields.Selection(string="Résultat Participation", selection=[('gagne', 'gagne'), ('perdu', 'perdu'),], required=False, )
    dotations = fields.Char(string="Dotations", required=False, )
    pers_inter_particip = fields.Many2one(comodel_name="person.interaction", string="Code Intéraction", required=False, )
    id_interaction_prtc = fields.Integer(related="pers_inter_particip.id", string="Identifiant Intéraction", required=False, )
    id_pers_cdp_prtc = fields.Char(related="pers_inter_particip.id_code_person", string="Identifiant Personne", required=False, )
    id_pers_marq_prtc = fields.Selection(related="pers_inter_particip.id_personne_marque", string="Identifiant Personne Marque", required=False, )
    id_cd_marq_prtc = fields.Many2one(related="pers_inter_particip.marque_code", string="Personne Marque", required=False, )
    id_cd_src_prtc = fields.Many2one(related="pers_inter_particip.source_code", string="Personne Source", required=False, )

class InteractionCommande(models.Model):
    _name = 'interaction.order'
    _rec_name = 'code_canal_cmd'

    date_commande = fields.Datetime(string="Date Commande", required=False, )
    code_canal_cmd = fields.Char(string="Code Canal Commande", required=True, )
    libelle_canal_cmd = fields.Selection(string="Libellé Canal Commande", selection=[('pnt_vente,', 'Point de vente'),('network,', 'réseaux'), ('sites', 'sites'), ], required=True, )
    nbr_articles = fields.Integer(string="Nombre d`\'articles", required=False, )
    sous_total_ht = fields.Float(string="Sous total HT",  required=False, )
    total_ht = fields.Float(string="Total HT", required=False, )
    total_tva = fields.Float(string="Total TVA", required=False, )
    total_cmd_ttc = fields.Float(string="Total Commande TTC", required=False, )
    mode_payement = fields.Selection(string="Mode de paiement", selection=[('CB', 'CB'),('Cheque', 'Chèque'), ('vir_sepa', 'virement SEPA'), ('prelev_sepa', 'prélèvement SEPA'),('liquide', 'Liquide'),], required=False, )
    status_cmd = fields.Selection(string="Status Commande", selection=[('payee', 'payée'),('rejet', 'rejet'), ('anulee', 'annulée'), ('en_att', 'en attente'),], required=False, )
    pers_inter_order = fields.Many2one(comodel_name="person.interaction", string="Code Intéraction", required=False, )
    id_interaction_cmd = fields.Integer(related="pers_inter_order.id", string="Identifiant Intéraction", required=False, )
    id_pers_cdp_cmd = fields.Char(related="pers_inter_order.id_code_person", string="Identifiant Personne", required=False, )
    id_pers_marq_cmd = fields.Selection(related="pers_inter_order.id_personne_marque", string="Identifiant Personne Marque", required=False, )
    id_cd_marq_cmd = fields.Many2one(related="pers_inter_order.marque_code", string="Personne Marque", required=False, )
    id_cd_src_cmd = fields.Many2one(related="pers_inter_order.source_code", string="Personne Source", required=False, )
    article_ids = fields.One2many(comodel_name="article.order", inverse_name="inter_cmd", string="Articles Commande", required=False, )


class ArticleCommande(models.Model):
    _name = 'article.order'
    _rec_name = 'libelle_article'

    inter_cmd = fields.Many2one(comodel_name="interaction.order", string="Code Canal Commande", required=False, )
    id_cmd = fields.Integer(related="inter_cmd.id", string="ID Commande", required=False, )
    nbr_lignes_cmd = fields.Integer(string="Nombre Lignes Commande", required=False, )
    ligne = fields.Char(string="Ligne", required=False, )
    code_article = fields.Char(string="Code article", required=False, )
    libelle_article = fields.Char(string="Libelle article", required=False, )
    qty_article = fields.Integer(string="Quantité article", required=False, )
    puht_article = fields.Float(string="Prix unitaire HT",  required=False, )
    remise_article = fields.Float(string="Remise article",  required=False, )


class InteractionCoupons(models.Model):
    _name = 'interaction.coupons'
    _rec_name = 'pers_inter_coupons'

    date_telechargement_coupon = fields.Date(string="Date Téléchrgement Coupon", required=False, )
    gencode_coupon = fields.Char(string="Code Coupon", required=True, )
    libelle_coupon = fields.Char(string="Libellé Coupon",required=False, )
    type_coupon = fields.Char(string="Type Coupon", required=False, )
    statut_usage_coupon = fields.Selection(string="Statut Usage Coupon", selection=[('oui', 'Oui'), ('non', 'Non'),], required=False, )
    lieu_usage_coupon = fields.Char(string="Lieu Usage Coupon", required=False, help="Code Postal")
    pers_inter_coupons = fields.Many2one(comodel_name="person.interaction", string="Code Intéraction", required=False, )
    id_interaction_cp = fields.Integer(related="pers_inter_coupons.id", string="Identifiant Intéraction", required=False, )
    id_pers_cdp_cp = fields.Char(related="pers_inter_coupons.id_code_person", string="Identifiant Personne", required=False, )
    id_pers_marq_cp = fields.Selection(related="pers_inter_coupons.id_personne_marque", string="Identifiant Personne Marque", required=False, )
    id_cd_marq_cp = fields.Many2one(related="pers_inter_coupons.marque_code", string="Personne Marque", required=False, )
    id_cd_src_cp = fields.Many2one(related="pers_inter_coupons.source_code", string="Personne Source", required=False, )

class InteractionSollicitation(models.Model):
    _name = 'interaction.sollicitation'
    _rec_name = 'nature_message_campagne'

    date_sollicitation_campagne = fields.Date(string="Date Sollicitation Compagne", required=False, )
    nature_message_campagne = fields.Selection(string="Nature Message Campagne", selection=[('gestion', 'gestion'),('marketing', 'marketing'),('marque', 'marque'),('rse', 'rse'), ], required=False,)
    objet_message_campagne = fields.Char(string="Objet message Campagne", required=False, )
    date_resultat_campagne = fields.Date(string="Date résultat Campagne", required=False, )
    resultat_campagne = fields.Selection(string="Résultat Campagne", selection=[('clic', 'clic'),('ouverture', 'ouverture'),('soft', 'soft'),('bounce', 'bounce'), ('hard', 'hard'), ('spam', 'spam'), ('plainte', 'plainte'), ('desabonnement', 'désabonnement'),], required=False,)
    lien_clique_campagne = fields.Char(string="Lien clique Compagne", required=False, )
    lien_1 = fields.Char(string=" Lien 1", required=False, )
    lien_2 = fields.Char(string="Lien 2", required=False, )
    lien_3 = fields.Char(string=" Lien 3", required=False, )
    pers_inter_sollic = fields.Many2one(comodel_name="person.interaction", string="Code Intéraction", required=False, )
    id_interaction_slc = fields.Integer(related="pers_inter_sollic.id", string="Identifiant Intéraction", required=False, )
    id_pers_cdp_slc = fields.Char(related="pers_inter_sollic.id_code_person", string="Identifiant Personne", required=False, )
    id_pers_marq_slc = fields.Selection(related="pers_inter_sollic.id_personne_marque", string="Identifiant Personne Marque", required=False, )
    id_cd_marq_slc = fields.Many2one(related="pers_inter_sollic.marque_code", string="Personne Marque", required=False, )
    id_cd_src_slc = fields.Many2one(related="pers_inter_sollic.source_code", string="Personne Source", required=False, )

class InteractionUsageService(models.Model):
    _name = 'interaction.usage.service'
    _rec_name = 'code_usage_serv'

    date_usage = fields.Datetime(string="Date Usage", required=False, )
    code_usage_serv = fields.Many2one(comodel_name="usage.service", string="Code Usage", required=True, )
    libelle_usage = fields.Char(related="code_usage_serv.libelle_usage", string="Libellé Usage", )
    valeur_usage = fields.Selection(string="Valeur Usage", selection=[('0', 'Oui'),('1', 'Non'), ], required=False, )
    pers_inter_us_service = fields.Many2one(comodel_name="person.interaction", string="Code Intéraction", required=False, )
    id_interaction_us_service = fields.Integer(related="pers_inter_us_service.id", string="Identifiant Intéraction", required=False, )
    id_pers_cdp_us_service = fields.Char(related="pers_inter_us_service.id_code_person", string="Identifiant Personne", required=False, )
    id_pers_marq_us_service = fields.Selection(related="pers_inter_us_service.id_personne_marque", string="Identifiant Personne Marque", required=False, )
    id_cd_marq_us_service = fields.Many2one(related="pers_inter_us_service.marque_code", string="Personne Marque", required=False, )
    id_cd_src_us_service = fields.Many2one(related="pers_inter_us_service.source_code", string="Personne Source", required=False, )

class InteractionContact(models.Model):
    _name = 'interaction.contact'
    _rec_name = 'pers_inter_contact'

    date_contact = fields.Datetime(string="Date Contact", required=False, )
    code_int_contact = fields.Many2one(comodel_name="contact.contact",string="Code Contact", required=True, )
    libelle_int_contact = fields.Char(related="code_int_contact.libelle_contact", string="Libellé Contact", )
    valeur_contact = fields.Selection(string="Valeur Contact", selection=[('0,', 'Non'),('1,', 'Oui'), ], required=False, )
    pers_inter_contact = fields.Many2one(comodel_name="person.interaction", string="Code Intéraction", required=False, )
    id_interaction_cnt = fields.Integer(related="pers_inter_contact.id", string="Identifiant Intéraction", required=False, )
    id_pers_cdp_cnt = fields.Char(related="pers_inter_contact.id_code_person", string="Identifiant Personne", required=False, )
    id_pers_marq_cnt = fields.Selection(related="pers_inter_contact.id_personne_marque", string="Identifiant Personne Marque", required=False, )
    id_cd_marq_cnt = fields.Many2one(related="pers_inter_contact.marque_code", string="Personne Marque", required=False, )
    id_cd_src_cnt = fields.Many2one(related="pers_inter_contact.source_code", string="Personne Source", required=False, )

class InteractionOffre(models.Model):
    _name = 'interaction.offre'
    _rec_name = 'pers_inter_offre'

    date_offre = fields.Datetime(string="Date Offre", required=False, )
    code_int_offre = fields.Many2one(comodel_name="offre.offre",string="Code Offre", required=True, )
    libelle_int_offre = fields.Char(related="code_int_offre.libelle_offre", string="Libellé Offre", )
    valeur_offre = fields.Selection(string="Valeur Offre", selection=[('0,', 'Non'),('1,', 'Oui'), ], required=False, )
    pers_inter_offre = fields.Many2one(comodel_name="person.interaction", string="Code Intéraction", required=False, )
    id_interaction_of = fields.Integer(related="pers_inter_offre.id", string="Identifiant Intéraction", required=False, )
    id_pers_cdp_of = fields.Char(related="pers_inter_offre.id_code_person", string="Identifiant Personne", required=False, )
    id_pers_marq_of = fields.Selection(related="pers_inter_offre.id_personne_marque", string="Identifiant Personne Marque", required=False, )
    id_cd_marq_of = fields.Many2one(related="pers_inter_offre.marque_code", string="Personne Marque", required=False, )
    id_cd_src_of = fields.Many2one(related="pers_inter_offre.source_code", string="Personne Source", required=False, )


class InteractionFideliteBurn(models.Model):
    _name = 'interaction.fidelite.burn'
    _rec_name = 'pers_inter_fidel'

    date_action_burn = fields.Datetime(string="Date action Burn", required=False, )
    nature_burn = fields.Selection(string="Nature Burn", selection=[('p', 'point'),('E', 'euros'), ], required=False, )
    code_article_burn = fields.Selection(string="Code article Burn", selection=[('br', 'BR'),('dotations', 'dotations'),('cagnotage', 'cagnotage'),('ba', 'BA'),], required=False, )
    affection_burn = fields.Float(string="Affectation Burn", required=False, )
    solde_compte_fidelite = fields.Float(string="Solde compte fidelité", required=False, )
    statut_membre = fields.Char(string="Statut membre", required=False, )
    pers_inter_fidel = fields.Many2one(comodel_name="person.interaction", string="Code Intéraction", required=False, )
    id_interaction_fidel = fields.Integer(related="pers_inter_fidel.id", string="Identifiant Intéraction", required=False, )
    id_pers_cdp_fidel = fields.Char(related="pers_inter_fidel.id_code_person", string="Identifiant Personne", required=False, )
    id_pers_marq_fidel = fields.Selection(related="pers_inter_fidel.id_personne_marque", string="Identifiant Personne Marque", required=False, )
    id_cd_marq_fidel = fields.Many2one(related="pers_inter_fidel.marque_code", string="Personne Marque", required=False, )
    id_cd_src_fidel = fields.Many2one(related="pers_inter_fidel.source_code", string="Personne Source", required=False, )

class InteractionFideliteEarn(models.Model):
    _name = 'interaction.fidelite.earn'
    _rec_name = 'pers_inter_fidel'

    date_action_earn = fields.Datetime(string="Date action Earn", required=False, )
    type_action_earn = fields.Selection(string="Type action Earn", selection=[('t', 'PA'),('E', 'Engagement'),('R', 'Relationnel'), ], required=False, )
    nb_pa = fields.Integer(string="Nombre PA", required=False, )
    nature_earn = fields.Selection(string="Nature Earn", selection=[('p', 'point'),('E', 'euros'), ], required=False, )
    affection_earn = fields.Float(string="Affectation Earn",  required=False, )
    solde_compte_fidelite = fields.Float(string="Solde compte fidelité",  required=False, )
    statut_membre = fields.Char(string="Statut membre", required=False, )
    pers_inter_fidel = fields.Many2one(comodel_name="person.interaction", string="Code Intéraction", required=False, )
    id_interaction_fidel = fields.Integer(related="pers_inter_fidel.id", string="Identifiant Intéraction", required=False, )
    id_pers_cdp_fidel = fields.Char(related="pers_inter_fidel.id_code_person", string="Identifiant Personne", required=False, )
    id_pers_marq_fidel = fields.Selection(related="pers_inter_fidel.id_personne_marque", string="Identifiant Personne Marque", required=False, )
    id_cd_marq_fidel = fields.Many2one(related="pers_inter_fidel.marque_code", string="Personne Marque", required=False, )
    id_cd_src_fidel = fields.Many2one(related="pers_inter_fidel.source_code", string="Personne Source", required=False, )






class Personne(models.Model):
    _name = 'person.person'
    _rec_name = 'id_cdp'

    marque_code = fields.Many2one(comodel_name="person.marque", string="Code marque", required=True, )
    marque_libelle = fields.Char(related="marque_code.libelle_marque", string="Libelle Marque", required=False, )
    source_code = fields.Many2one(comodel_name="person.source", string="Code source", required=True, )
    source_libelle = fields.Char(related="source_code.libelle_source", string="Libelle source", required=False, )
    id_cdp = fields.Char(string="Identifiant", required=False, )
    id_personne_marque = fields.Char(string="", required=False, )
    type_id_marque = fields.Char(string="", required=False, )
    type_personne = fields.Selection(string="Type personne", selection=[('PP', ' PERSPONNE PHYSIQUE'), ('PM', ' PERSONNE MORALE'), ], required=False, )
    statut_personne = fields.Selection(string="Statut personne", selection=[('00', 'PROSPECT'), ('01', 'CLIENT'),('02', 'CANDIDAT'), ('03', ' FRANCHISE POTENTIEL'), ], required=False, )
    libelle_statut_personne = fields.Char(string="Libelle statut", required=False, )
    role_personne = fields.Selection(string="", selection=[('reprentant PM', 'reprentant PM'), ('aidant', 'aidant'), ], required=False, )
    fonction_personne = fields.Char(string="Fonction personne", required=False, )

