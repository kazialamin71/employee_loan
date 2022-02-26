from openerp.osv import fields, osv
from openerp import api
from openerp.tools.translate import _
from datetime import date, time

class Leih_loan(osv.osv):
    _name = "leih.loan"
    _inherit="loan.abst"

    _columns = {

        'name': fields.char("Display Name"),
        'payment_schedule_id':fields.one2many("loan.in_payment",'loan_id',"Payment Schedule ID"),

    }

    def confirm_loan(self, cr, uid, ids, context=None):

        loan_obj = self.browse(cr, uid, [ids[0]], context=context)
        interest_period=0
        # check if before there are balance
        hr_loan_ids=loan_obj.employee_id.hr_employee_loan_ids
        if len(hr_loan_ids)>0:
            len_loan=len(hr_loan_ids)-1
            last_balance=hr_loan_ids[len_loan].balance
        else:
            last_balance=0
        emp_id=loan_obj.employee_id.id
        loan_id=loan_obj.id
        total_loan=loan_obj.loan_amount
        total_balance=last_balance+total_loan
        request_date=loan_obj.request_date
        total_emi_no=len(loan_obj.payment_schedule_id)
        interest_period=loan_obj.interest_period
        first_payment_date=loan_obj.first_payment_date
        total_with_interest=loan_obj.total_principle_amount


        for item in loan_obj.payment_schedule_id:
            installment_amount=item.installment_amount
            last_date=item.schedule_date
        contract_id=self.pool.get('hr.contract').search(cr, uid, [('employee_id','=', emp_id)], context=context)[0]
        contract_obj=self.pool.get('hr.contract').browse(cr, uid, contract_id, context=context)
        cr.execute('update hr_contract set loan_amount=%s,remaining_loan=%s,no_of_emi=%s,remaining_emi=%s,monthly_loan=%s,first_payment_date=%s,last_payment_date=%s where id=%s', (total_with_interest,total_with_interest,total_emi_no,total_emi_no,installment_amount,first_payment_date,last_date,contract_id))
        cr.commit()
        emp_loan_value = {
            'hr_employee_id': emp_id,
            'loan': total_loan,
            'balance': total_balance,
            'given_loan': total_loan,
            'date':request_date,
            'loan_id':loan_id
        }
        emp_obj = self.pool.get('hr.employee.loan')
        loan_obj_id = emp_obj.create(cr, uid, emp_loan_value, context=context)

        return True



    def loan_cancel(self, cr, uid, ids, context=None):

        loan_obj = self.browse(cr, uid, [ids[0]], context=context)
        loan_id=loan_obj.id

        interest_period=0
        # check if before there are balance
        hr_loan_ids=loan_obj.employee_id.hr_employee_loan_ids
        # import pdb
        # pdb.set_trace()
        if len(hr_loan_ids)>0:
            cr.execute('delete from hr_employee_loan where loan_id=%s',([loan_id]))
            cr.commit()

        return True


    def pay_loan(self, cr, uid, ids, context=None):

        loan_obj = self.browse(cr, uid, [ids[0]], context=context)

        return True

    def create(self, cr, uid, vals, context=None):
        stored = super(Leih_loan, self).create(cr, uid, vals, context) # return ID int object


        if stored is not None:
            name_text = 'Loan-' + str(stored)
            cr.execute('update leih_loan set name=%s where id=%s', (name_text, stored))
            cr.commit()
        return stored


class LoanInPayment(osv.osv):
    _name = "loan.in_payment"
    _inherit = "common.payment.schedule"

    _columns = {
        'loan_id':fields.many2one("leih.loan"),
        # 'employee_id':fields.many2one("hr.employee",related='loan_id.employee_id')
    }
    # @api.model
    # def create(self, vals):
    #     import pdb
    #     pdb.set_trace()


