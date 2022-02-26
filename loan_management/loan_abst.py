
from openerp.osv import fields, osv
from openerp import api
from openerp.tools.translate import _
from datetime import date, time, datetime
from dateutil import relativedelta


class Loan_abst(osv.AbstractModel):
    _name = "loan.abst"
    #
    # @api.multi
    # def _compute_total(self):
    #     value={}
    #     for record in self:
    #         value[record.id]=1
    #     return value

    _columns = {

        'name': fields.char("Name"),
        'maximum_loan':fields.integer('Maximum Loan'),
        'company_id':fields.many2one("res.company","Company"),
        'employee_id':fields.many2one("hr.employee","Employee"),
        'request_date':fields.date("Request Date"),
        'type_id':fields.selection([('pf','PF'),('personal','Personal')],string="Loan Type", default='pf'),
        'loan_amount':fields.float("Loan Amount"),
        'previous_loan_amount':fields.float(string='Previous Loan'),
        'maximum_loan_amount':fields.float("Maximum Loan Amount"),
        'interest':fields.integer("Interest"),
        'interest_period':fields.integer("Interest(Peroid)"),
        'merge_loan':fields.boolean("Merge Loan"),
        'maximum_installment_period':fields.integer("Maximum Installment Period"),
        'manual_loan_period':fields.integer("Loan Period"),
        'first_payment_date':fields.date("First Payment Date"),
        'total_principle_amount':fields.integer("Total Amount"),
        'total_interest_amount':fields.integer("First Payment Date"),
        # 'total_principle_amount':fields.function(_compute_total,"Total Principle Amount"),
        # 'total_interest_amount':fields.function(_compute_total,"Total Interest Amount"),
        'payment_schedule_id':fields.one2many("loan.in_payment",'loan_id'),
        'state':fields.selection([('draft','Draft'),('confirm','Confirm'),('active','Active')],string="State")

    }

    @api.onchange('employee_id')
    def onchange_emp(self):
        employee_id=self.employee_id
        previous_loan=0
        len_loan_list=len(self.employee_id.hr_employee_loan_ids)
        if len_loan_list>0:
            last_loan_obj=employee_id.hr_employee_loan_ids[len_loan_list-1]
            previous_loan=last_loan_obj.balance
        self.previous_loan_amount=previous_loan


    @api.multi
    def action_compute_payment(self):
        for loan in self:
            loan._compute_payment()

    @api.multi
    def _compute_payment(self):
        self.ensure_one()
        schedule_object_name = self.payment_schedule_id._name
        obj_payment = self.env[schedule_object_name]
        # import pdb
        # pdb.set_trace()

        self.payment_schedule_id.unlink()

        payment_datas = self._compute_flat(
            self.loan_amount,
            self.previous_loan_amount,
            self.interest,
            self.interest_period,
            self.manual_loan_period,
            self.first_payment_date
        )

        for payment_data in payment_datas:
            payment_data.update({"loan_id": self.id})
            obj_payment.create(payment_data)

    @api.model
    def _compute_flat(self, loan_amount,previous_loan, interest,interest_period, period, first_payment_date):
        result = []
        loan_now=loan_amount
        if previous_loan>0:
            loan_amount=loan_amount+previous_loan
        if interest_period>0:
            interest_period=interest_period
        else:
            interest_period=0
        principle_amount = loan_amount / period
        total_principle_amount = principle_amount*(interest_period+period)
        self.env.cr.execute("update leih_loan set total_principle_amount=%s where id=%s",
                   (total_principle_amount, self.id))
        self.env.cr.commit()
        interest_amount = (loan_now * (interest / 100.00))/period
        next_payment_date = datetime.strptime(first_payment_date, "%Y-%m-%d")
        if interest_period>period:
            raise osv.except_osv(_('Error!'),
                                 _("Check the period and interest period"))
        else:
            for _loan_period in range(1, period + 1+interest_period):
                res = {
                    "schedule_date": next_payment_date.strftime("%Y-%m-%d"),
                    "principle_amount": principle_amount,
                    "interest_amount": interest_amount,
                    "installment_amount":principle_amount+interest_amount,
                }
                result.append(res)
                next_payment_date = next_payment_date + relativedelta.relativedelta(months=+1)

        return result


    # _defaults={
    #     'company_id':lambda self: self._default_company_id(),
    # }