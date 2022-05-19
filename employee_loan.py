import pdb

from openerp.osv import fields, osv
from openerp.tools.translate import _
from datetime import date, time
from openerp import api


class EmployeeLoan(osv.osv):
    _name = "employee.loan"


    _columns = {

        'name': fields.char("Name"),
        'employee_id': fields.many2one("hr.employee","Employee"),
        'loan_amount': fields.float("Loan Amount"),
        'confirmed_loan_amount': fields.float("Confirmed Amount"),
        'loan_rate': fields.float("Loan Rate (%)"),
        'type': fields.selection([('pf', 'PF'), ('personal', 'Personal')], 'Loan Type'),
        'emi_no': fields.float("Total No EMI"),
        'pay_amount_periodical': fields.float("Periodical Amount Monthly"),
        'loan_payble_amount': fields.float("Loan Payble By Employee"),
        'loan_disburse_date': fields.date("Loan Disburse Date"),
        'loan_last_payment_date': fields.date("Last Payment Date"),
        'state': fields.selection(
            [('pending', 'Pending'), ('confirm', 'Confirmed'), ('cancelled', 'Cancelled')],
            'Status', default='pending', readonly=True,
        ),
    }

    @api.onchange('emi_no')
    def loan_payable(self):
        loan_payable_amount=0
        if self.emi_no:
            total_addition=(self.loan_amount*self.loan_rate)/100
            loan_payable_amount=self.loan_amount+total_addition
            periodical=loan_payable_amount/self.emi_no
            self.pay_amount_periodical=periodical
            self.loan_payble_amount=loan_payable_amount
        return 'X'


    # def change_status(self,cr,uid,ids,context=None):
    #     loan_obj=self.browse(cr,uid,ids,context=context)
    #     if loan_obj.state=="confirm":
    #         raise osv.except_osv(_('Warning!'),
    #                              ("The Loan is already confirmed"))
    #
    #
    #     employee_id=loan_obj.employee_id
    #     loan_amount=loan_obj.loan_payble_amount
    #     periodical_amount=loan_obj.pay_amount_periodical
    #     last_payment_date=loan_obj.loan_last_payment_date
    #     contract_id=self.pool.get("hr.contract").search(cr, uid, [('employee_id', '=', employee_id.id)], context=context)
    #     contract_obj=self.pool.get("hr.contract").browse(cr,uid,contract_id[0],context)
    #     contract_vals={
    #         'x_loan_amount':loan_amount,
    #         'x_loan_kisti':periodical_amount,
    #         'x_last_payment_date':last_payment_date,
    #         'x_emi_no':loan_obj.emi_no,
    #         'x_remaining_emi':loan_obj.emi_no
    #     }
    #     change=self.pool.get("hr.contract").write(cr,uid,[contract_id[0]],contract_vals,context)
    #
    #
    #     if change==True:
    #         cr.execute("update employee_loan set state='confirm' where id=%s",(ids))
    #         cr.commit()
    #         hr_employee_loan_ids = []
    #
    #         loan_profile_upudate = {
    #             'hr_employee_id':loan_obj.employee_id.id,
    #             'date':loan_obj.loan_disburse_date,
    #             'pf':0,
    #             'loan':loan_obj.loan_payble_amount,
    #             'given_loan':loan_obj.loan_amount,
    #             'taken_loan':loan_obj.loan_payble_amount,
    #             'balance':loan_obj.loan_payble_amount,
    #
    #         }
    #
    #         # hr_employee_loan_ids.append((1, 1, {
    #         #     'loan': loan_amount
    #         # }))
    #         # l_vals = {
    #         #     'hr_employee_loan_ids': hr_employee_loan_ids
    #         # }
    #         changes = self.pool.get("hr.employee.loan").create(cr, uid, loan_profile_upudate, context)
    #     return "X"




class hr_payslip(osv.osv):
    _inherit = 'hr.payslip'

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        contract_obj = self.pool.get("hr.contract").browse(cr, uid, [vals['contract_id']], context)
        remaining_emi=contract_obj.remaining_emi
        remaining_loan=contract_obj.remaining_loan
        if remaining_emi>0:
            monthly_loan=contract_obj.monthly_loan
            new_remaining_loan=remaining_loan-monthly_loan
            emp_id=contract_obj.employee_id.id
            emp_obj = self.pool.get("hr.employee").browse(cr, uid, emp_id, context)
            len_loan=len(emp_obj.hr_employee_loan_ids)
            last_index=len_loan-1
            last_balance=emp_obj.hr_employee_loan_ids[last_index].balance
            new_balance=last_balance-monthly_loan
            #if monthly loan is greater than remaining loan
            if monthly_loan>new_remaining_loan:
                monthly_loan=new_remaining_loan
                new_balance = last_balance - new_remaining_loan
                new_remaining_loan = monthly_loan-remaining_loan
                #end
            if remaining_emi>0:
                new_remaining_emi=remaining_emi-1

                cr.execute("update hr_contract set remaining_emi=%s,remaining_loan=%s where id=%s", (new_remaining_emi,new_remaining_loan,vals['contract_id']))
                cr.commit()
                emp_loan_value = {
                    'hr_employee_id': emp_id,
                    'loan': monthly_loan,
                    'taken_loan': monthly_loan,
                    'balance': new_balance,
                    'date': date.today()
                }
                emp_obj = self.pool.get('hr.employee.loan')
                loan_obj_id = emp_obj.create(cr, uid, emp_loan_value, context=context)
        return super(hr_payslip, self).create(cr, uid, vals, context=context)

    #code for cpf loan on payslip rules
    # result = (contract.monthly_loan) if contract.remaining_emi > 0 else inputs.CPFLOAN.amount


    # if contract.remaining_emi > 0 and contract.remaining_loan >= contract.monthly_loan:
    #     result = (contract.monthly_loan)
    # elif contract.remaining_emi > 0 and contract.remaining_loan < contract.monthly_loan:
    #     result = (contract.remaining_loan)
    # else:
    #     result = inputs.CPFLOAN.amount

    # result = inputs.CPFLOAN.amount


#
# class hr_employee(osv.osv):
#     _inherit = 'hr.employee'
#
#     def write(self, cr, uid,ids, vals, context=None):
#         import pdb
#         pdb.set_trace()
