class DomainError(Exception):
    """Base for all business-rule violations.

    Raised in the service layer; never in routes or repositories.
    The web layer maps each subclass to an HTTP status code.
    """


class PaymentNotFound(DomainError):
    def __init__(self, payment_id: int) -> None:
        self.payment_id = payment_id
        super().__init__(f"Payment {payment_id} not found")


class DuplicatePaymentNumber(DomainError):
    def __init__(self, number: str) -> None:
        self.number = number
        super().__init__(f"Payment with number '{number}' already exists")


class InvalidPaymentAmount(DomainError):
    pass
