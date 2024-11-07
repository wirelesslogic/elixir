from enum import Enum


class CustomerStatus(Enum):
    LOST = 0
    PROSPECT = 1
    CUSTOMER = 2

    @staticmethod
    def from_str(label):
        mapping = {
            "lost": CustomerStatus.LOST,
            "prospect": CustomerStatus.PROSPECT,
            "customer": CustomerStatus.CUSTOMER,
        }
        return mapping.get(label.lower(), None)


class EmailCategory(Enum):
    ALERT = 0
    NOTIFICATION = 1
    MARKETING = 2

    @staticmethod
    def from_str(label):
        mapping = {
            "alert": EmailCategory.ALERT,
            "notification": EmailCategory.NOTIFICATION,
            "marketing": EmailCategory.MARKETING,
        }
        return mapping.get(label.lower(), None)


class LabelCategory(Enum):
    CUSTOM = 0
    OPERATOR = 1
    PRODUCT = 2

    @staticmethod
    def from_str(label):
        label = label.lower()
        if label == "custom":
            return LabelCategory.CUSTOM
        elif label == "operator":
            return LabelCategory.OPERATOR
        elif label == "product":
            return LabelCategory.PRODUCT
        else:
            raise ValueError(f"Invalid label category: {label}")

    @staticmethod
    def from_str(label):
        mapping = {
            "custom": LabelCategory.CUSTOM,
            "operator": LabelCategory.OPERATOR,
            "product": LabelCategory.PRODUCT,
        }
        return mapping.get(label.lower(), None)


class MailStatus(Enum):
    PENDING = 0
    ACCEPTED = 1
    REJECTED = 2
    DELIVERED = 3
    FAILED = 4
    OPENED = 5
    COMPLAINED = 6
    STORED = 7

    @staticmethod
    def from_str(label):
        mapping = {
            "pending": MailStatus.PENDING,
            "accepted": MailStatus.ACCEPTED,
            "rejected": MailStatus.REJECTED,
            "delivered": MailStatus.DELIVERED,
            "failed": MailStatus.FAILED,
            "opened": MailStatus.OPENED,
            "complained": MailStatus.COMPLAINED,
            "stored": MailStatus.STORED,
        }
        return mapping.get(label.lower(), None)
