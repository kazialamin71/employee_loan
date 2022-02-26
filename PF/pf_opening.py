import pdb

from openerp.osv import fields, osv
from openerp.tools.translate import _
from datetime import date, time
from openerp import api


class pfopening(osv.osv):
    _name = "pf.opening"

    def _balance(self, cr, uid, ids, fieldnames, args, context=None):
        """For each hr.attendance record of action sign-in: assign 0.
        For each hr.attendance record of action sign-out: assign number of hours since last sign-in.
        """
        res = {}
        for record in self.browse(cr, uid, ids, context=context):
            emp=record.emp_contribution
            com=record.com_contribution
            total_amount=emp+com
            res[record.id]=total_amount
        return res


    _columns = {

        'name': fields.char("Name"),
        'employee_id': fields.many2one("hr.employee","Employee"),
        'emp_contribution': fields.float("EMP Contribution"),
        'com_contribution': fields.float("Com Contribution"),
        'balance': fields.function(_balance, type='float', string='Balnace', store=True),
        'state': fields.selection(
            [('pending', 'Pending'), ('confirm', 'Confirmed'), ('cancelled', 'Cancelled')],
            'Status', default='pending', readonly=True,
        )
    }

    def confirm_pf(self, cr, uid, ids, context=None):

        pf_obj = self.browse(cr, uid, [ids[0]], context=context)
        interest_period=0
        # check if before there are balance
        hr_pf_ids=pf_obj.employee_id.hr_employee_pf_id
        if len(hr_pf_ids)>0:
            len_pf=len(hr_pf_ids)-1
            last_balance=hr_pf_ids[len_pf].balance
        else:
            last_balance=0
        emp_id=pf_obj.employee_id.id
        emp_contribution=pf_obj.emp_contribution
        com_contribution=pf_obj.com_contribution
        balance=pf_obj.balance
        emp_pf_value = {
            'hr_employee_id': emp_id,
            'emp_contribution': emp_contribution,
            'com_contribution': com_contribution,
            'balance': balance,

        }
        emp_obj = self.pool.get('hr.employee.pf')
        pf_obj_id = emp_obj.create(cr, uid, emp_pf_value, context=context)

        return True


    def pay_loan(self, cr, uid, ids, context=None):

        loan_obj = self.browse(cr, uid, [ids[0]], context=context)

        return True
