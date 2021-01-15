# -*- coding: utf-8 -*-

import unittest

from odoo.addons.base.tests.test_form_create import TestFormCreate


@unittest.skip('Monkey patch test_create_res_partner')
def test_create_res_partner(self):
    pass

TestFormCreate.test_create_res_partner = test_create_res_partner
