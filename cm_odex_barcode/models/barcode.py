# -*- coding: utf-8 -*-

# import sys
#
# # reload(sys)
# # sys.setdefaultencoding("utf-8")
import base64
import os

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from io import BytesIO
from lxml import etree

import arabic_reshaper
from bidi.algorithm import get_display
from odoo import models, api, fields
from odoo.tools.translate import _
from odoo.osv.orm import setup_modifiers


class Transaction(models.Model):
    _inherit = 'transaction.transaction'

    binary_barcode = fields.Binary(string='Barcode', attachment=True)

    @api.multi
    @api.constrains('ean13', 'name', 'transaction_date', 'type')
    def binary_compute_constraint(self):
        fonts = [os.path.dirname(__file__) + '/img/KacstOffice.ttf',
                 os.path.dirname(__file__) + '/img/amiri-regular.ttf']
        img = Image.new("RGBA", (300, 220), "white")
        draw = ImageDraw.Draw(img)
        number_word = "الرقم : "
        number_word_reshaped = arabic_reshaper.reshape(
            u'' + number_word)
        number_word_artext = get_display(number_word_reshaped)
        draw.text((230, 20),
                  number_word_artext, "black",
                  font=ImageFont.truetype(fonts[1], 18))

        number_value = self.name
        number_value_reshaped = arabic_reshaper.reshape(
            u'' + number_value if number_value else '')
        number_value_artext = get_display(number_value_reshaped)
        draw.text((110, 20),
                  number_value_artext, "black",
                  font=ImageFont.truetype(fonts[1], 18))
        #
        date_hijri = "التاريخ : "
        date_hijri_reshaped = arabic_reshaper.reshape(
            u'' + date_hijri)
        date_hijri_artext = get_display(date_hijri_reshaped)
        draw.text((230, 40),
                  date_hijri_artext, "black",
                  font=ImageFont.truetype(fonts[1], 18))

        date_hijri_value = self.transaction_date_hijri
        date_hijri_value_reshaped = arabic_reshaper.reshape(
            u'' + date_hijri_value if date_hijri_value else '')
        date_hijri_artext = get_display(date_hijri_value_reshaped)
        draw.text((130, 40),
                  date_hijri_artext.replace('-', '/'), "black",
                  font=ImageFont.truetype(fonts[1], 18))

        date_m = "الموافق : "
        date_m_reshaped = arabic_reshaper.reshape(
            u'' + date_m)
        date_m_artext = get_display(date_m_reshaped)
        draw.text((230, 60),
                  date_m_artext, "black",
                  font=ImageFont.truetype(fonts[1], 18))

        date_m_value = self.transaction_date
        date_m_value_reshaped = arabic_reshaper.reshape(
            u'' + date_m_value if date_m_value else '')
        date_m_value_artext = get_display(date_m_value_reshaped)
        draw.text((130, 60),
                  date_m_value_artext.replace('-', '/'), "black",
                  font=ImageFont.truetype(fonts[1], 18))

        attach_m = "المرفقات : "
        attach_m_reshaped = arabic_reshaper.reshape(
            u'' + attach_m)
        date_m_artext = get_display(attach_m_reshaped)
        draw.text((230, 80),
                  date_m_artext, "black",
                  font=ImageFont.truetype(fonts[1], 18))

        attach_m_value = str(self.attachment_num) if self.attachment_num else '0'
        attach_m_value_reshaped = arabic_reshaper.reshape(
            u'' + attach_m_value)
        attach_mvalue_artext = get_display(attach_m_value_reshaped)
        draw.text((180, 80),
                  attach_mvalue_artext, "black",
                  font=ImageFont.truetype(fonts[1], 18))
        barcode = self.env['ir.actions.report'].barcode('Code128', self.name, width=250, height=100,
                                             humanreadable=0)
        barcode_buffer = BytesIO(barcode)
        barcode_image_file = Image.open(barcode_buffer)
        ImageDraw.Draw(img)
        buffered = BytesIO()
        img.paste(barcode_image_file, (20, 110))
        img.save(buffered, format="png")
        img_str = base64.b64encode(buffered.getvalue())
        self.binary_barcode = img_str

    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     """
    #     overrides open erp field view get to to dynamically set invisible, readonly and required attributes
    #     on fields according to user security access
    #     fields_view_get([view_id | view_type='form'])
    #
    #     Get the detailed composition of the requested view like fields, model, view architecture
    #
    #     :param view_id: id of the view or None
    #     :param view_type: type of the view to return if view_id is None ('form', 'tree', ...)
    #     :param toolbar: true to include contextual actions
    #     :param submenu: deprecated
    #
    #     :return: dictionary describing the composition of the requested view (including inherited views and extensions)
    #
    #     :raise AttributeError:
    #             * if the inherited view has unknown position to work with other than 'before', 'after', 'inside', 'replace'
    #             * if some tag other than 'position' is found in parent view
    #     :raise Invalid ArchitectureError: if there is view type other than form, tree, calendar, search etc defined on the structure
    #     """
    #     res = super(Transaction, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
    #                                                   submenu=submenu)
    #     doc = etree.XML(res['arch'])
    #     for node in doc.xpath("//button[@name='print_barcode']"):
    #         node.set('attrs', "{'invisible': [('create_uid','!=',%s)]}" % self.env.uid)
    #         setup_modifiers(node)
    #     res['arch'] = etree.tostring(doc)
    #     return res
