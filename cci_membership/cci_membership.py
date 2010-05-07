# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from osv import fields, osv
import datetime

class res_partner(osv.osv):
    _inherit = 'res.partner'
    _description = 'Partner'

    def _membership_state_job(self, cr, uid, ids=False, context={}):
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        membership_line_ids = self.pool.get('membership.membership_line').search(cr, uid, ['|', ('date_to','=', yesterday), ('date_from','=', today)], context=context)
        partner_tmp_ids = self.pool.get('membership.membership_line').read(cr, uid, membership_line_ids, ['partner'], context=context)
        partner_ids = partner_tmp_ids and map(lambda x:x['partner'][0],partner_tmp_ids) or False
        if partner_ids:
            self.write(cr, uid, partner_ids, {}, context)
        return True

    def _membership_vcs(self, cr, uid, ids, field_name=None, arg=None, context={}):
        '''To obtain the ID of the partner in the form of a belgian VCS for a membership offer'''
        res = {}
        for id in ids:
            value_digits = 1000000000 + id
            check_digits = value_digits % 97
            if check_digits == 0:
                check_digits = 97
            pure_string = str(value_digits) + ( str(check_digits).zfill(2) )
            res[id] = '***' + pure_string[0:3] + '/' + pure_string[3:7] + '/' + pure_string[7:] + '***'
        return res

    def _membership_state(self, cr, uid, ids, name, args, context=None):
        res = super(res_partner, self)._membership_state(cr, uid, ids, name, args, context)
        for partner in self.browse(cr, uid, ids, context):
            if partner.refuse_membership:
                res[partner.id] = 'canceled'
        return res

    _columns = {
        'membership_vcs': fields.function( _membership_vcs, method=True,string='VCS number for membership offer', type='char', size=20),
        'refuse_membership': fields.boolean('Refuse to Become a Member'),
    }

    _default = {
        'refuse_membership': lambda *a: 0,
    }

res_partner()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

