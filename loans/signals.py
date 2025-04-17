def update_loan_finished_payment(sender, instance, created, **kwargs):
    loan = instance.loan

    if loan.outstanding_balance <= instance.amount:
        loan.is_already_paid = True
        loan.save(update_fields=["is_already_paid"])
