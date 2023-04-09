# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime


class CrmPerson(models.Model):
    _name = 'crm.lead'
    _inherit = 'crm.lead'

    marque_code = fields.Many2one(comodel_name="person.marque", label="Code marque", required=False, )
    marque_libelle = fields.Char(related="marque_code.libelle_marque", label="Libelle Marque", required=False, )
    source_code = fields.Many2one(comodel_name="person.source", label="Code source", required=False, )
    source_libelle = fields.Char(related="source_code.libelle_source", label="Libelle source", required=False, )
    id_cdp = fields.Char(compute='_compute_id', label="Identifiant", required=False, )
    prenom = fields.Char(string="", required=False, )
    civilite = fields.Selection(string="", selection=[('M', 'M'), ('Mr', 'Mr'), ('MME', 'MME'), ], required=False, )
    date_creation = fields.Date(string="", required=False, )
    id_personne_marque = fields.Char(label="Identifiant Personne Marque", required=False, )
    type_id_marque = fields.Selection(label="ID Type Marque",
                                      selection=[('base_annonceur', 'base annonceur'), ('mobile', 'Mobile'), ('email', 'Email'), ('erp', 'Erp'), ('ss', 'SS'),
                                                 ('media', 'Media'), ('uid', 'uid')], required=False, )
    type_personne = fields.Selection(label="Type personne",
                                     selection=[('PP', ' PERSPONNE PHYSIQUE'), ('PM', ' PERSONNE MORALE'), ],
                                     required=False, )
    statut_personne = fields.Selection(label="Statut",
                                       selection=[('SP01', 'PROSPECT'), ('SP02', 'CLIENT'), ('SP03', 'MEMBRE'),
                                                  ('SP04', 'CANDIDAT'), ('SP05', 'FRANCHISE'), ('SP06', 'PARTICIPANT'), ('SP07', 'ANCIEN PARTICIPANT')], required=False, )
    libelle_statut_personne = fields.Char(label="Libelle statut", required=False, )
    role_personne = fields.Selection(label="", selection=[('reprentant PM', 'Reprentant PM'), ('aidant', 'Aidant'), ],
                                     required=False, )
    fonction_personne = fields.Char(label="Fonction", required=False, )
    origine_recrutement = fields.Many2one(comodel_name="origine.recrutement", label="Origine recrutement", required=False, )
    code_point_de_vente = fields.Char(label="Code point de vente", required=False, )
    libelle_point_de_vente = fields.Char(label="Libelle point de vente", required=False, )
    type_point_de_vente = fields.Selection(label="Type point de vente",
                                           selection=[('I', 'Intégré'), ('F', 'Franchisé'), ],
                                           required=False, )
    secteur_activite_societe = fields.Char(label="Secteur d'activité de socièté", required=False, )
    secteur_societe = fields.Char(label="Secteur de socièté", required=False, )
    date_naissance = fields.Date(label="Date de naissance", required=False, )
    acceptation_cgu = fields.Boolean(label="Acceptation CGU", )
    date_acceptation_cgu = fields.Datetime(label="Date d'acceptation CGU", required=False, )
    affectation = fields.Datetime(label="Date Affectation", required=False, )
    regime_matrimonial = fields.Char(label="Régime matrimonial", required=False, )
    composition_foyer = fields.Integer(label="Composition foyer", required=False, )
    date_naissance_conjoint = fields.Date(label="Date naissance conjoint", required=False, )
    date_naissance_enfant1 = fields.Date(label="Date naissance enfant 1", required=False, )
    date_naissance_enfant2 = fields.Date(label="Date naissance enfant 2", required=False, )
    date_naissance_enfant3 = fields.Date(label="Date naissance enfant 3", required=False, )
    interaction_ids = fields.One2many(comodel_name="person.interaction", inverse_name="lead_id", label="Intéractions", required=False, )

    statut_membre = fields.Char(label="Statut membre", required=False, )
    solde_compte_fidelite = fields.Float(label="Solde compte fidelité", required=False, selection=[('t', 'PA'), ('E', 'Engagement'), ('R', 'Relationnel'), ], )
    cumul_pa = fields.Float(label="", required=False, )
    cumul_earn = fields.Float(label="", required=False, )
    cumul_burn = fields.Float(label="", required=False, )
    cumul_participations = fields.Float(label="", required=False, )
    cumul_telechargement_coupon = fields.Float(label="", required=False, )
    cumul_usage_coupon = fields.Float(label="", required=False, )
    cumul_sollicitations = fields.Float(label="", required=False, )
    cumul_interactions = fields.Float(label="", required=False, )
    age = fields.Integer(label="Age", required=False, )
    lead_creation_dt = fields.Char(string="creation Date", compute="_creation_date")
    is_new = fields.Integer(string="Welcome value", required=False, compute="_isNew")
    is_birthday = fields.Integer(string="Birthday", required=False)
    birthday_computed = fields.Integer(string="En mode anniversaire", required=False, compute="_birthday_computed", store=True)
    birthday_recomputed = fields.Integer(string="En mode anniversaire 2", required=False, compute="_birthday_computed2", store=True)
    birthday_recomputedmonth = fields.Integer(string="En mode anniversaire MONTH", required=False, compute="_birthday_computed3", store=True)
    birthday_month = fields.Integer(string="BIRTHDAY MONTH", required=False, compute="_birthday_computed4", store=True)
    abn_dt = fields.Integer(string="Abonnement_dt", required=False, compute="_abn_date")
    cumul_pa = fields.Integer("Cumul PA", compute='_compute_cumul_pa', store=True)
    total_coupon = fields.Integer("Cumul téléchargement coupon", compute='_compute_total_coupon', store=True)
    total_coupon_used = fields.Integer("Cumul usage coupon", compute='_compute_total_coupon', store=True)
    nombre_coupon_telecharger = fields.Integer(
        compute='_compute_coupon_usage_download', store=True)
    nombre_coupon_utiliser = fields.Integer(
        compute='_compute_coupon_usage_download', store=True)

    @api.depends('interaction_ids', 'interaction_ids.inter_coupons',
                 'interaction_ids.inter_coupons.statut_usage_coupon')
    def _compute_coupon_usage_download(self):
        for this in self:
            coupon_downloaded = this.interaction_ids.inter_coupons.filtered(
                lambda c: c.date_telechargement_coupon)
            coupon_used = coupon_downloaded.filtered(
                lambda c: c.statut_usage_coupon == 'oui')
            this.update({
                'nombre_coupon_telecharger': len(coupon_downloaded),
                'nombre_coupon_utiliser': len(coupon_used)
            })

    @api.depends('interaction_ids', 'interaction_ids.inter_fidel_earns')
    def _compute_cumul_pa(self):
        for this in self:
            fidelite = self.env.ref('odoomoduleyes.intera_id_11', raise_if_not_found=False)
            fidelite_interactions = this.interaction_ids.filtered(lambda i: i.interaction == fidelite)
            earns = fidelite_interactions.mapped('inter_fidel_earns.nb_pa')
            this.cumul_pa = sum(earns)

    @api.depends('interaction_ids', 'interaction_ids.inter_coupons')
    def _compute_total_coupon(self):
        for this in self:
            coupon = self.env.ref('odoomoduleyes.intera_id_03', raise_if_not_found=False)
            fidelite_coupons = this.interaction_ids.filtered(
                lambda i: i.interaction == coupon)
            inter_coupons = fidelite_coupons.mapped('inter_coupons')
            this.total_coupon = len(inter_coupons)
            this.total_coupon_used = len(inter_coupons.filtered(lambda c: c.statut_usage_coupon == 'oui'))

    @api.depends('marque_code.code_marque')
    def _compute_id(self):
        for record in self:
            record.id_cdp = record.id
            if record.marque_code.code_marque:
                record.id_cdp = record.marque_code.code_marque + str(record.id)

    @api.depends('date_creation')
    def _creation_date(self):
        for record in self:
            record.lead_creation_dt = str(datetime.strptime(str(record.date_creation), "%Y-%m-%d")) if record.date_creation else False

    @api.depends('lead_creation_dt')
    def _isNew(self):
        for record in self:
            record.is_new = 0
            if record.lead_creation_dt:
                if record.lead_creation_dt == str(datetime.strptime(datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d")):
                    record.is_new = 1

    @api.depends('date_naissance')
    def _birthday_computed(self):
        for record in self:
            record.birthday_computed = 0
            if record.date_naissance:
                date_naiss = datetime.strptime(str(record.date_naissance), "%Y-%m-%d")
                mnt = date_naiss.month
                day = date_naiss.day
                current_date = datetime.now()
                if current_date.month == mnt and current_date.day == day:
                    record.birthday_computed = 1

    @api.depends('date_naissance')
    def _birthday_computed2(self):
        for record in self:
            record.birthday_recomputed = 0
            if record.date_naissance:
                date_naiss = datetime.strptime(str(record.date_naissance), "%Y-%m-%d")
                mnt = date_naiss.month
                day = date_naiss.day
                current_date = datetime.now()
                if current_date.month == mnt and current_date.day == day:
                    record.birthday_recomputed = 1

    @api.depends('date_naissance')
    def _birthday_computed3(self):
        for record in self:
            record.birthday_recomputedmonth = 0
            if record.date_naissance:
                date_naiss = datetime.strptime(str(record.date_naissance), "%Y-%m-%d")
                mnt = date_naiss.month
                day = date_naiss.day
                current_date = datetime.now()
                if current_date.month == mnt and current_date.day == day:
                    record.birthday_recomputedmonth = 1

    @api.depends('date_naissance')
    def _birthday_computed4(self):
        for record in self:
            record.birthday_month = 0
            if record.date_naissance:
                date_naiss = datetime.strptime(str(record.date_naissance), "%Y-%m-%d")
                mnt = date_naiss.month
                day = date_naiss.day
                current_date = datetime.now()
                record.birthday_month = mnt

    @api.depends('interaction_ids')
    def _abn_date(self):
        for record in self:
            record.abn_dt = 0
            res = self.env["interaction.abonnement"].search([('pers_inter_abn.lead_id','=',record.id)], limit=1).date_abn
            if res:
                abn = datetime.strptime(res.strftime("%Y-%m-%d"), "%Y-%m-%d")
                mnt = abn.month
                day = abn.day
                current_date = datetime.now()
                if current_date.month == mnt and current_date.day == day:
                    record.abn_dt = 1


class Interaction(models.Model):
    _name = 'person.interaction'
    _rec_name = 'code_interaction'

    date_interaction = fields.Date(label="Date Intéraction", required=False, )
    interaction = fields.Many2one(comodel_name="interaction.interaction", label="Libellé Intéraction", required=False, )
    code_interaction = fields.Char(related="interaction.code_interaction", label="Code Intéraction", required=False, )
    type_interaction = fields.Char(compute="_get_type_interaction", label="Type Intéraction", required=False, )
    libelle_type_interaction = fields.Char(compute="_get_libelle_type_interaction", label="Libellé Type Intéraction", required=False, )
    valeur_interaction = fields.Selection(label="Valeur Intéraction", selection=[('0', 'Oui'), ('1', 'Non'), ('9', 'Pas de réponse'), ], required=False, )
    lead_id = fields.Many2one(comodel_name="crm.lead", required=True, ondelete='cascade', )
    id_code_person = fields.Char(related="lead_id.id_cdp", label="Identifiant Personne", required=False, )
    id_personne_marque = fields.Char(related="lead_id.id_personne_marque", required=False, )
    marque_code = fields.Many2one(related="lead_id.marque_code", label="Code marque", required=False, )
    source_code = fields.Many2one(related="lead_id.source_code", label="Code source", required=False, )
    inter_cnstm = fields.One2many(comodel_name="interaction.consentement", inverse_name="pers_inter_cons", label="Consentements", required=False, )
    inter_abnms = fields.One2many(comodel_name="interaction.abonnement", inverse_name="pers_inter_abn", label="Abonnements", required=False, )
    inter_prtcps = fields.One2many(comodel_name="interaction.participation", inverse_name="pers_inter_particip", label="Participations", required=False, )
    inter_orders = fields.One2many(comodel_name="interaction.order", inverse_name="pers_inter_order", label="Commandes", required=False, )
    inter_coupons = fields.One2many(comodel_name="interaction.coupons", inverse_name="pers_inter_coupons", label="Coupons", required=False, )
    inter_sollicits = fields.One2many(comodel_name="interaction.sollicitation", inverse_name="pers_inter_sollic", label="Sollicitations", required=False, )
    inter_us_services = fields.One2many(comodel_name="interaction.usage.service", inverse_name="pers_inter_us_service", label="Usages des services",
                                        required=False, )
    inter_contacts = fields.One2many(comodel_name="interaction.contact", inverse_name="pers_inter_contact", label="Contacts", required=False, )
    inter_offres = fields.One2many(comodel_name="interaction.offre", inverse_name="pers_inter_offre", label="Offres", required=False, )
    inter_fidel_earns = fields.One2many(comodel_name="interaction.fidelite.earn", inverse_name="pers_inter_fidel", label="Fidelité Earn", required=False, )
    inter_fidel_burns = fields.One2many(comodel_name="interaction.fidelite.burn", inverse_name="pers_inter_fidel", label="Fidelité Burn", required=False, )

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

    code_marque = fields.Char(label="Code marque", required=True, )
    libelle_marque = fields.Char(label="Libellé marque", required=False, )


class Source(models.Model):
    _name = 'person.source'
    _rec_name = 'code_source'

    code_source = fields.Char(label="Code Source", required=True, )
    libelle_source = fields.Char(label="Libellé Source", required=False, )


class OrigineRecrutement(models.Model):
    _name = 'origine.recrutement'
    _rec_name = 'code_origine'

    code_origine = fields.Char(label="Code Origine", required=True, )
    libelle_origine = fields.Char(label="Libellé Origine", required=False, )


class LeadInteraction(models.Model):
    _name = 'interaction.interaction'
    _rec_name = 'libelle_interaction'

    code_interaction = fields.Char(label="Code Intéraction", required=True, )
    libelle_interaction = fields.Char(label="Libellé Intéraction", required=False, )


class Consentement(models.Model):
    _name = 'consentement.consentement'
    _rec_name = 'code_consentement'

    code_consentement = fields.Char(label="Code Consentement", required=True, )
    libelle_consentement = fields.Char(label="Libellé Consentement", required=False, )


class Abonnement(models.Model):
    _name = 'abonnement.abonnement'
    _rec_name = 'code_abonnement'

    code_abonnement = fields.Char(label="Code Abonnement", required=True, )
    libelle_abonnement = fields.Char(label="Libellé Abonnement", required=False, )


class Participation(models.Model):
    _name = 'participation.participation'
    _rec_name = 'code_participation'

    code_participation = fields.Char(label="Code Participation", required=True, )
    libelle_participation = fields.Char(label="Libellé Participation", required=False, )


class UsageService(models.Model):
    _name = 'usage.service'
    _rec_name = 'code_usage'

    code_usage = fields.Char(label="Code Usage", required=True, )
    libelle_usage = fields.Char(label="Libellé Usage", required=False, )


class Contacts(models.Model):
    _name = 'contact.contact'
    _rec_name = 'code_contact'

    code_contact = fields.Char(label="Code Contact", required=True, )
    libelle_contact = fields.Char(label="Libellé Contact", required=False, )


class Offres(models.Model):
    _name = 'offre.offre'
    _rec_name = 'code_offre'

    code_offre = fields.Char(label="Code Offre", required=True, )
    libelle_offre = fields.Char(label="Libellé Offre", required=False, )


class InteractionConsentement(models.Model):
    _name = 'interaction.consentement'
    _rec_name = 'pers_inter_cons'

    date_cnstm = fields.Date(label="Date Consentement", required=False, )
    code_cnstm = fields.Many2one(comodel_name="consentement.consentement", label="Code Consentement", required=False, )
    libelle_cnstm = fields.Char(related="code_cnstm.libelle_consentement", label="Libellé Consentement", )
    support_cnstm = fields.Selection(label="Support Consentement", selection=[('e-mail', 'e-mail'), ('mobile', 'mobile'), ('telephone', 'téléphone'), ],
                                     required=False, )
    valeur_cnstm = fields.Selection(label="Valeur Consentement", selection=[('0', 'OPT-IN NON'), ('1', 'OPT-IN OUI'), ('9', 'OUTPUT'), ], required=False, )
    pers_inter_cons = fields.Many2one(comodel_name="person.interaction", label="Code Intéraction", required=False, )
    id_interaction = fields.Integer(related="pers_inter_cons.id", label="Identifiant Intéraction", required=False, )
    id_pers_cdp = fields.Char(related="pers_inter_cons.id_code_person", label="Identifiant Personne", required=False, )
    id_pers_marq = fields.Char(related="pers_inter_cons.id_personne_marque", label="Identifiant Personne Marque", required=False, )
    id_cd_marq = fields.Many2one(related="pers_inter_cons.marque_code", label="Personne Marque", required=False, )
    id_cd_src = fields.Many2one(related="pers_inter_cons.source_code", label="Personne Source", required=False, )


class InteractionAbonnement(models.Model):
    _name = 'interaction.abonnement'
    _rec_name = 'pers_inter_abn'

    date_abn = fields.Datetime(label="Date Abonnement", required=False, )
    code_abn = fields.Many2one(comodel_name="abonnement.abonnement", label="Code Abonnement", required=False, )
    libelle_abn = fields.Char(related="code_abn.libelle_abonnement", label="Libellé Abonnement", )
    cordonnee_abn = fields.Selection(label="Cordonnées Abonnement", selection=[('email', 'email'), ('mobile', 'mobile'), ('telephone', 'téléphone'), ],
                                     required=False, )
    valeur_abn = fields.Selection(label="Valeur Consentement", selection=[('0', 'NON'), ('1', 'OUI'), ], required=False, )
    pers_inter_abn = fields.Many2one(comodel_name="person.interaction", label="Code Intéraction", required=False, )
    id_interaction_abn = fields.Integer(related="pers_inter_abn.id", label="Identifiant Intéraction", required=False, )
    id_pers_cdp_abn = fields.Char(related="pers_inter_abn.id_code_person", label="Identifiant Personne", required=False, )
    id_pers_marq_abn = fields.Char(related="pers_inter_abn.id_personne_marque", label="Identifiant Personne Marque", required=False, )
    id_cd_marq_abn = fields.Many2one(related="pers_inter_abn.marque_code", label="Personne Marque", required=False, )
    id_cd_src_abn = fields.Many2one(related="pers_inter_abn.source_code", label="Personne Source", required=False, )


class InteractionParticipation(models.Model):
    _name = 'interaction.participation'
    _rec_name = 'pers_inter_particip'

    date_participation = fields.Datetime(label="Date Participation", required=False, )
    code_operation = fields.Many2one(comodel_name="participation.participation", label="Code Opération", required=False, )
    libelle_operation = fields.Char(related="code_operation.libelle_participation", label="Libellé Opération", )
    type_operation = fields.Selection(label="Type Opération", selection=[('blog', 'blog'),('tas', 'tas'),('odr', 'odr'),('jeux', 'jeux'), ('concours,', 'concours'), ('activation', 'activation'), ],
                                      required=False, )
    res_participation = fields.Selection(label="Résultat Participation", selection=[('Gagne', 'Gagne'), ('Perdu', 'Perdu'), ], required=False, )
    dotations = fields.Char(label="Dotations", required=False, )
    id_participation = fields.Char(string="", required=False, )
    conformite_participation = fields.Char(string="", required=False, )
    pers_inter_particip = fields.Many2one(comodel_name="person.interaction", label="Code Intéraction", required=False, )
    id_interaction_prtc = fields.Integer(related="pers_inter_particip.id", label="Identifiant Intéraction", required=False, )
    id_pers_cdp_prtc = fields.Char(related="pers_inter_particip.id_code_person", label="Identifiant Personne", required=False, )
    id_pers_marq_prtc = fields.Char(related="pers_inter_particip.id_personne_marque", label="Identifiant Personne Marque", required=False, )
    id_cd_marq_prtc = fields.Many2one(related="pers_inter_particip.marque_code", label="Personne Marque", required=False, )
    id_cd_src_prtc = fields.Many2one(related="pers_inter_particip.source_code", label="Personne Source", required=False, )


class InteractionCommande(models.Model):
    _name = 'interaction.order'
    _rec_name = 'code_canal_cmd'

    date_commande = fields.Datetime(label="Date Commande", required=False, )
    code_canal_cmd = fields.Char(label="Code Canal Commande", required=False, )
    libelle_canal_cmd = fields.Selection(label="Libellé Canal Commande",
                                         selection=[('pnt_vente,', 'Point de vente'), ('network,', 'réseaux'), ('sites', 'sites'), ], required=False, )
    nbr_articles = fields.Integer(label="Nombre d`\'articles", required=False, )
    sous_total_ht = fields.Float(label="Sous total HT", required=False, )
    total_ht = fields.Float(label="Total HT", required=False, )
    total_tva = fields.Float(label="Total TVA", required=False, )
    total_cmd_ttc = fields.Float(label="Total Commande TTC", required=False, )
    mode_payement = fields.Selection(label="Mode de paiement",
                                     selection=[('CB', 'CB'), ('Cheque', 'Chèque'), ('vir_sepa', 'virement SEPA'), ('prelev_sepa', 'prélèvement SEPA'),
                                                ('liquide', 'Liquide'), ], required=False, )
    status_cmd = fields.Selection(label="Status Commande", selection=[('payee', 'payée'), ('rejet', 'rejet'), ('anulee', 'annulée'), ('en_att', 'en attente'), ],
                                  required=False, )
    pers_inter_order = fields.Many2one(comodel_name="person.interaction", label="Code Intéraction", required=False, )
    id_interaction_cmd = fields.Integer(related="pers_inter_order.id", label="Identifiant Intéraction", required=False, )
    id_pers_cdp_cmd = fields.Char(related="pers_inter_order.id_code_person", label="Identifiant Personne", required=False, )
    id_pers_marq_cmd = fields.Char(related="pers_inter_order.id_personne_marque", label="Identifiant Personne Marque", required=False, )
    id_cd_marq_cmd = fields.Many2one(related="pers_inter_order.marque_code", label="Personne Marque", required=False, )
    id_cd_src_cmd = fields.Many2one(related="pers_inter_order.source_code", label="Personne Source", required=False, )
    article_ids = fields.One2many(comodel_name="article.order", inverse_name="inter_cmd", label="Articles Commande", required=False, )


class ArticleCommande(models.Model):
    _name = 'article.order'
    _rec_name = 'libelle_article'

    inter_cmd = fields.Many2one(comodel_name="interaction.order", label="Code Canal Commande", required=False, )
    id_cmd = fields.Integer(related="inter_cmd.id", label="ID Commande", required=False, )
    nbr_lignes_cmd = fields.Integer(label="Nombre Lignes Commande", required=False, )
    ligne = fields.Char(label="Ligne", required=False, )
    code_article = fields.Char(label="Code article", required=False, )
    libelle_article = fields.Char(label="Libelle article", required=False, )
    qty_article = fields.Integer(label="Quantité article", required=False, )
    puht_article = fields.Float(label="Prix unitaire HT", required=False, )
    remise_article = fields.Float(label="Remise article", required=False, )


class InteractionCoupons(models.Model):
    _name = 'interaction.coupons'
    _rec_name = 'pers_inter_coupons'

    date_telechargement_coupon = fields.Date(label="Date Téléchrgement Coupon", required=False, )
    gencode_coupon = fields.Char(label="Gen Code Coupon", required=False, )
    code_coupon = fields.Char(label="Code Coupon", required=False, )
    libelle_coupon = fields.Char(label="Libellé Coupon", required=False, )
    type_coupon = fields.Char(label="Type Coupon", required=False, )
    statut_usage_coupon = fields.Selection(label="Statut Usage Coupon", selection=[('oui', 'Oui'), ('non', 'Non'), ], required=False, )
    lieu_usage_coupon = fields.Char(label="Lieu Usage Coupon", required=False)
    enseigne_usage_coupon = fields.Char(label="Enseigne Usage Coupon", required=False)
    pers_inter_coupons = fields.Many2one(comodel_name="person.interaction", label="Code Intéraction", required=False, )
    id_interaction_cp = fields.Integer(related="pers_inter_coupons.id", label="Identifiant Intéraction", required=False, )
    id_pers_cdp_cp = fields.Char(related="pers_inter_coupons.id_code_person", label="Identifiant Personne", required=False, )
    id_pers_marq_cp = fields.Char(related="pers_inter_coupons.id_personne_marque", label="Identifiant Personne Marque", required=False, )
    id_cd_marq_cp = fields.Many2one(related="pers_inter_coupons.marque_code", label="Personne Marque", required=False, )
    id_cd_src_cp = fields.Many2one(related="pers_inter_coupons.source_code", label="Personne Source", required=False, )


class InteractionSollicitation(models.Model):
    _name = 'interaction.sollicitation'
    _rec_name = 'nature_message_campagne'

    date_sollicitation_campagne = fields.Date(label="Date Sollicitation Compagne", required=False, )
    nature_message_campagne = fields.Selection(label="Nature Message Campagne",
                                               selection=[('gestion', 'gestion'), ('marketing', 'marketing'), ('marque', 'marque'), ('rse', 'rse'), ],
                                               required=False, )
    objet_message_campagne = fields.Char(label="Objet message Campagne", required=False, )
    date_resultat_campagne = fields.Date(label="Date résultat Campagne", required=False, )
    resultat_campagne = fields.Selection(label="Résultat Campagne",
                                         selection=[('clic', 'clic'), ('ouverture', 'ouverture'), ('soft', 'soft'), ('bounce', 'bounce'), ('hard', 'hard'),
                                                    ('spam', 'spam'), ('plainte', 'plainte'), ('desabonnement', 'désabonnement'), ], required=False, )
    lien_clique_campagne = fields.Char(label="Lien clique Compagne", required=False, )
    lien_1 = fields.Char(label=" Lien 1", required=False, )
    lien_2 = fields.Char(label="Lien 2", required=False, )
    lien_3 = fields.Char(label=" Lien 3", required=False, )
    pers_inter_sollic = fields.Many2one(comodel_name="person.interaction", label="Code Intéraction", required=False, )
    id_interaction_slc = fields.Integer(related="pers_inter_sollic.id", label="Identifiant Intéraction", required=False, )
    id_pers_cdp_slc = fields.Char(related="pers_inter_sollic.id_code_person", label="Identifiant Personne", required=False, )
    id_pers_marq_slc = fields.Char(related="pers_inter_sollic.id_personne_marque", label="Identifiant Personne Marque", required=False, )
    id_cd_marq_slc = fields.Many2one(related="pers_inter_sollic.marque_code", label="Personne Marque", required=False, )
    id_cd_src_slc = fields.Many2one(related="pers_inter_sollic.source_code", label="Personne Source", required=False, )


class InteractionUsageService(models.Model):
    _name = 'interaction.usage.service'
    _rec_name = 'code_usage_serv'

    date_usage = fields.Datetime(label="Date Usage", required=False, )
    code_usage_serv = fields.Many2one(comodel_name="usage.service", label="Code Usage", required=False, )
    libelle_usage = fields.Char(related="code_usage_serv.libelle_usage", label="Libellé Usage", )
    valeur_usage = fields.Selection(label="Valeur Usage", selection=[('0', 'Oui'), ('1', 'Non'), ], required=False, )
    pers_inter_us_service = fields.Many2one(comodel_name="person.interaction", label="Code Intéraction", required=False, )
    id_interaction_us_service = fields.Integer(related="pers_inter_us_service.id", label="Identifiant Intéraction", required=False, )
    id_pers_cdp_us_service = fields.Char(related="pers_inter_us_service.id_code_person", label="Identifiant Personne", required=False, )
    id_pers_marq_us_service = fields.Char(related="pers_inter_us_service.id_personne_marque", label="Identifiant Personne Marque", required=False, )
    id_cd_marq_us_service = fields.Many2one(related="pers_inter_us_service.marque_code", label="Personne Marque", required=False, )
    id_cd_src_us_service = fields.Many2one(related="pers_inter_us_service.source_code", label="Personne Source", required=False, )


class InteractionContact(models.Model):
    _name = 'interaction.contact'
    _rec_name = 'pers_inter_contact'

    date_contact = fields.Datetime(label="Date Contact", required=False, )
    code_int_contact = fields.Many2one(comodel_name="contact.contact", label="Code Contact", required=False, )
    libelle_int_contact = fields.Char(related="code_int_contact.libelle_contact", label="Libellé Contact", )
    valeur_contact = fields.Selection(label="Valeur Contact", selection=[('0,', 'Non'), ('1,', 'Oui'), ], required=False, )
    pers_inter_contact = fields.Many2one(comodel_name="person.interaction", label="Code Intéraction", required=False, )
    id_interaction_cnt = fields.Integer(related="pers_inter_contact.id", label="Identifiant Intéraction", required=False, )
    id_pers_cdp_cnt = fields.Char(related="pers_inter_contact.id_code_person", label="Identifiant Personne", required=False, )
    id_pers_marq_cnt = fields.Char(related="pers_inter_contact.id_personne_marque", label="Identifiant Personne Marque", required=False, )
    id_cd_marq_cnt = fields.Many2one(related="pers_inter_contact.marque_code", label="Personne Marque", required=False, )
    id_cd_src_cnt = fields.Many2one(related="pers_inter_contact.source_code", label="Personne Source", required=False, )


class InteractionOffre(models.Model):
    _name = 'interaction.offre'
    _rec_name = 'pers_inter_offre'

    date_offre = fields.Datetime(label="Date Offre", required=False, )
    code_int_offre = fields.Many2one(comodel_name="offre.offre", label="Code Offre", required=False, )
    libelle_int_offre = fields.Char(related="code_int_offre.libelle_offre", label="Libellé Offre", )
    valeur_offre = fields.Selection(label="Valeur Offre", selection=[('0,', 'Non'), ('1,', 'Oui'), ], required=False, )
    pers_inter_offre = fields.Many2one(comodel_name="person.interaction", label="Code Intéraction", required=False, )
    id_interaction_of = fields.Integer(related="pers_inter_offre.id", label="Identifiant Intéraction", required=False, )
    id_pers_cdp_of = fields.Char(related="pers_inter_offre.id_code_person", label="Identifiant Personne", required=False, )
    id_pers_marq_of = fields.Char(related="pers_inter_offre.id_personne_marque", label="Identifiant Personne Marque", required=False, )
    id_cd_marq_of = fields.Many2one(related="pers_inter_offre.marque_code", label="Personne Marque", required=False, )
    id_cd_src_of = fields.Many2one(related="pers_inter_offre.source_code", label="Personne Source", required=False, )


class InteractionFideliteBurn(models.Model):
    _name = 'interaction.fidelite.burn'
    _rec_name = 'pers_inter_fidel'

    date_action_burn = fields.Datetime(label="Date action Burn", required=False, )
    nature_burn = fields.Selection(label="Nature Burn", selection=[('P', 'point'), ('E', 'euros'), ], required=False, )
    code_article_burn = fields.Selection(label="Code article Burn",
                                         selection=[('Br', 'BR'), ('dotations', 'dotations'), ('cagnotage', 'cagnotage'), ('BA', 'BA'), ], required=False, )
    affection_burn = fields.Char(label="Affectation Burn", required=False, )
    solde_compte_fidelite = fields.Char(label="Solde compte fidelité", required=False, )
    statut_membre = fields.Char(label="Statut membre", required=False, )
    pers_inter_fidel = fields.Many2one(comodel_name="person.interaction", label="Code Intéraction", required=False, )
    id_interaction_fidel = fields.Integer(related="pers_inter_fidel.id", label="Identifiant Intéraction", required=False, )
    id_pers_cdp_fidel = fields.Char(related="pers_inter_fidel.id_code_person", label="Identifiant Personne", required=False, )
    id_pers_marq_fidel = fields.Char(related="pers_inter_fidel.id_personne_marque", label="Identifiant Personne Marque", required=False, )
    id_cd_marq_fidel = fields.Many2one(related="pers_inter_fidel.marque_code", label="Personne Marque", required=False, )
    id_cd_src_fidel = fields.Many2one(related="pers_inter_fidel.source_code", label="Personne Source", required=False, )


class InteractionFideliteEarn(models.Model):
    _name = 'interaction.fidelite.earn'
    _rec_name = 'pers_inter_fidel'

    date_action_earn = fields.Datetime(label="Date action Earn", required=False, )
    type_action_earn = fields.Selection(label="Type action Earn", selection=[('T', 'T'), ('E', 'Engagement'), ('R', 'Relationnel'), ], required=False, )
    nb_pa = fields.Integer(label="Nombre PA", required=False, )
    nature_earn = fields.Selection(label="Nature Earn", selection=[('P', 'point'), ('E', 'euros'), ], required=False, )
    affection_earn = fields.Char(label="Affectation Earn", required=False, )
    solde_compte_fidelite = fields.Char(label="Solde compte fidelité", required=False, )
    statut_membre = fields.Char(label="Statut membre", required=False, )
    pers_inter_fidel = fields.Many2one(comodel_name="person.interaction", label="Code Intéraction", required=False, )
    id_interaction_fidel = fields.Integer(related="pers_inter_fidel.id", label="Identifiant Intéraction", required=False, )
    id_pers_cdp_fidel = fields.Char(related="pers_inter_fidel.id_code_person", label="Identifiant Personne", required=False, )
    id_pers_marq_fidel = fields.Char(related="pers_inter_fidel.id_personne_marque", label="Identifiant Personne Marque", required=False, )
    id_cd_marq_fidel = fields.Many2one(related="pers_inter_fidel.marque_code", label="Personne Marque", required=False, )
    id_cd_src_fidel = fields.Many2one(related="pers_inter_fidel.source_code", label="Personne Source", required=False, )


class Personne(models.Model):
    _name = 'person.person'
    _rec_name = 'id_cdp'

    marque_code = fields.Many2one(comodel_name="person.marque", label="Code marque", required=True, )
    marque_libelle = fields.Char(related="marque_code.libelle_marque", label="Libelle Marque", required=False, )
    source_code = fields.Many2one(comodel_name="person.source", label="Code source", required=True, )
    source_libelle = fields.Char(related="source_code.libelle_source", label="Libelle source", required=False, )
    id_cdp = fields.Char(label="Identifiant", required=False, )
    id_personne_marque = fields.Char(label="", required=False, )
    type_id_marque = fields.Char(label="", required=False, )
    type_personne = fields.Selection(label="Type personne", selection=[('PP', ' PERSPONNE PHYSIQUE'), ('PM', ' PERSONNE MORALE'), ], required=False, )
    statut_personne = fields.Selection(label="Statut personne",
                                       selection=[('00', 'PROSPECT'), ('01', 'CLIENT'), ('02', 'CANDIDAT'), ('03', ' FRANCHISE POTENTIEL'), ], required=False, )
    libelle_statut_personne = fields.Char(label="Libelle statut", required=False, )
    role_personne = fields.Selection(label="", selection=[('reprentant PM', 'reprentant PM'), ('aidant', 'aidant'), ], required=False, )
    fonction_personne = fields.Char(label="Fonction personne", required=False, )


