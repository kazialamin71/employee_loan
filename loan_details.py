from openerp.osv import fields, osv
from openerp.tools.translate import _
from datetime import date, time
from openerp import api
from openerp import SUPERUSER_ID


class LoanDetails(osv.osv):
    _inherit = 'hr.employee'

    def _loan_count(self, cr, uid, ids, field_name, arg, context=None):
        Contract = self.pool['leih.loan']
        return {
            employee_id: Contract.search_count(cr, SUPERUSER_ID, [('employee_id', '=', employee_id)], context=context)
            for employee_id in ids

        }


    _columns = {

        'hr_employee_loan_ids': fields.one2many('hr.employee.loan','hr_employee_id',"Name"),
        'hr_employee_pf_id':fields.one2many('hr.employee.pf','hr_employee_id','PF'),
        'loan_count': fields.function(_loan_count, type='integer', string='Loan')
    }



class hr_employee_loan(osv.osv):
    _name = "hr.employee.loan"

    _columns = {
        'hr_employee_id':fields.many2one('hr.employee','Hr Employee'),
        'date':fields.date("Date"),
        'pf':fields.float("PF"),
        'loan':fields.float("Loan"),
        'given_loan':fields.float("Given Loan"),
        'interest':fields.float("Interest"),
        'taken_loan':fields.float("Taken Loan"),
        'balance':fields.float("Balance"),
        'loan_id':fields.many2one("leih.loan","Loan ID")
    }

class hr_employee_pf(osv.osv):
    _name = "hr.employee.pf"

    _columns = {
        'hr_employee_id':fields.many2one('hr.employee','Hr Employee'),
        'date':fields.date("Date"),
        'emp_contribution':fields.float("Employee Contribution"),
        'com_contribution':fields.float("Company Contribution"),
        'total_amount':fields.float("Total Amount"),
        'balance':fields.float("Balance")
    }

class hr_contract(osv.osv):
    _inherit = 'hr.contract'

    _columns = {
        'loan_amount': fields.float("Loan Amount"),
        'remaining_loan':fields.float("Remaining Loan"),
        'no_of_emi': fields.integer('No of Total EMI'),
        'remaining_emi': fields.integer('Remaining EMI'),
        'monthly_loan': fields.float('Monthly Loan'),
        'first_payment_date': fields.date('First Payment Date'),
        'last_payment_date':fields.date("Last Payment Date"),
        'pf_account_id':fields.many2one("account.account","PF Account"),
        'loan_account_id':fields.many2one("account.account","Loan Account"),
        'gins_account_id':fields.many2one("account.account","Group Insurance Account"),
    }



