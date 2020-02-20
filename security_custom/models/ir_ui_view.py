from odoo import api, fields, models


class View(models.Model):
    _inherit = 'ir.ui.view'

    def _apply_group(self, model, node, modifiers, fields):
        """Apply group restrictions,  may be set at view level or model level::
           * at view level this means the element should be made invisible to
             people who are not members
           * at model level (exclusively for fields, obviously), this means
             the field should be completely removed from the view, as it is
             completely unavailable for non-members

           :return: True if field should be included in the result of fields_view_get

           #custom
           add readonly_groups feature
        """
        Model = self.env[model]

        can_see = can_read = 'not seted'
        if node.tag == 'field' and node.get('name') in Model._fields:
            field = Model._fields[node.get('name')]
            if field.groups and not self.user_has_groups(groups=field.groups):
                node.getparent().remove(node)
                fields.pop(node.get('name'), None)
                # no point processing view-level ``groups`` anymore, return
                return False
        if node.get('groups'):
            can_see = self.user_has_groups(groups=node.get('groups'))
            if not can_see:
                node.set('invisible', '1')
                modifiers['invisible'] = True
            del node.attrib['groups']

        if node.get('readonly_groups'):
            can_read = self.user_has_groups(groups=node.get('readonly_groups'))
            if can_read and not can_see:
                node.set('invisible', '0')
                modifiers['invisible'] = False
                node.set('readonly', '1')
                modifiers['readonly'] = True
            del node.attrib['readonly_groups']

        if can_see == False and can_read == False:
            if 'attrs' in node.attrib:
                del node.attrib['attrs']    # avoid making field visible later

        return True
