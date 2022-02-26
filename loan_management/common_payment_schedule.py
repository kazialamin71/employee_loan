from openerp.osv import fields, osv
from openerp import api
from openerp.tools.translate import _
from datetime import date, time

class Common_payment_schedule(osv.AbstractModel):
    _name = "common.payment.schedule"

    # @api.multi
    # @api.depends("principle_amount", "interest_amount")
    # def _compute_installment(self):
    #     compute_installment={}
    #     for payment in self:
    #         compute_installment[payment.id] = payment.principle_amount + payment.interest_amount
    #     return compute_installment


    _columns = {

        'name': fields.char("Display Name"),
        'loan_id':fields.many2one("loan.abst","Loan ABst"),
        'employee_id':fields.many2one("hr.employee","Employee"),
        'schedule_date':fields.date("Schedule Date"),
        'principle_amount':fields.float("Principle Amount"),
        'interest_amount':fields.float("Interest Amount"),
        # 'installment_amount':fields.function(_compute_installment,string="Total Principle Amount",type='float'),
        'installment_amount':fields.float(string="Installment Amount"),
        'principle_payment_state':fields.selection([("unpaid", "Unpaid"),("paid", "Paid")],string="Payment State", default="unpaid"),
        'state':fields.selection([("draft", "Draft"),("confirm", "Confirm"),("cancel","Cancel")],string="Payment State"),
  }
