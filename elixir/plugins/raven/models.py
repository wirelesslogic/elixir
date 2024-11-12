# app/plugins/raven/models.py
from datetime import datetime

from elixir.db.base_models import WiLoModel
from elixir.db.custom_fields import EnumField, JsonField

from elixir.core.enums import CustomerStatus
from peewee import (
    CharField,
    DateTimeField,
    ForeignKeyField,
    TextField,
    DateField,
    IntegerField,
    DecimalField,
    SmallIntegerField,
)


# ======================================================================
# Plugin Models
# ======================================================================
class Customers(WiLoModel):
    account_manager = CharField(null=True)
    action_date = DateField(null=True)
    action_required = CharField(null=True)
    activation_ready = CharField()
    billing_code = CharField(null=True)
    bundle_trigger_mail = CharField(null=True)
    category = CharField(null=True)
    comment = CharField(null=True)
    contact_person = CharField(null=True)
    contract = CharField()
    contract_term_kpn = IntegerField()
    contract_term_tele2 = IntegerField()
    contract_term_telenor = IntegerField()
    contract_term_tmobile = IntegerField()
    contract_term_vodafone = IntegerField()
    contract_term_conexa_ld = IntegerField()
    contract_term_conexa_os = IntegerField()
    customer_name = CharField(index=True)
    cloud_environment = CharField(null=True)
    phone_number = CharField(null=True)
    shipping_fee = DecimalField(8, 2)
    status = EnumField(
        choices=CustomerStatus, default=CustomerStatus.CUSTOMER, index=True
    )
    subscription_package = CharField(null=True)
    support_24x7 = CharField()
    support_contact = CharField(null=True)
    support_mail = CharField(null=True)
    support_phone = CharField(null=True)
    test_customer = CharField()
    test_ready_period_kpn = IntegerField()
    test_ready_period_tele2 = IntegerField()
    test_ready_period_telenor = IntegerField()
    test_ready_period_tmobile = IntegerField()
    test_ready_period_vodafone = IntegerField()
    test_ready_period_conexa_ld = IntegerField()
    test_ready_period_conexa_os = IntegerField()
    vat_code = SmallIntegerField(null=True)
    vat_number = CharField(null=True)
    vat_tariff = SmallIntegerField(null=True)
    direct_debit = SmallIntegerField(default=0)
    iban = CharField(null=True)
    swift = CharField(null=True)
    payment_method = CharField(null=True)
    payment_days = SmallIntegerField(default=90)
    invoice_mail = CharField()
    invoice_template = CharField(null=True)
    salesforce_id = CharField(null=True)
    purchase_order_reference = CharField(null=True)
    created = DateTimeField(default=datetime.now)
    updated = DateTimeField(default=datetime.now)

    class Meta:
        table_name = "customers"


class CustomerAddresses(WiLoModel):
    customer = ForeignKeyField(model=Customers, backref="addresses")
    category = CharField(max_length=10)
    name = CharField(null=True)
    address = CharField(null=True)
    city = CharField(null=True)
    postal_code = CharField(null=True)
    country = CharField(null=True)

    class Meta:
        table_name = "customer_addresses"
        indexes = ((("customer", "category"), True),)


class CustomerIPRanges(WiLoModel):
    customer = ForeignKeyField(model=Customers, backref="ip_ranges")
    customer_range = CharField()
    operator = CharField(max_length=20)
    operator_uuid = CharField(max_length=20)
    free_ips = IntegerField(null=True)

    class Meta:
        table_name = "customer_ip_ranges"


class CustomerSpecials(WiLoModel):
    customer = ForeignKeyField(model=Customers, backref="specials")
    specials = JsonField()
    category = CharField(max_length=10)
    subcategory = CharField(max_length=10)
    jasper = SmallIntegerField(default=0)

    class Meta:
        table_name = "customer_specials"


# class Email(WiLoModel):
#     customer = ForeignKeyField(Customer, backref="emails", on_delete="CASCADE")
#     email_address = CharField(max_length=255)
#     category = EnumField(EmailCategory, index=True)

#     class Meta:
#         table_name = "raven_emails"


# class Label(WiLoModel):
#     name = CharField(max_length=50)
#     category = EnumField(LabelCategory, index=True)

#     class Meta:
#         table_name = "raven_labels"


# class Concept(WiLoModel):
#     name = CharField(max_length=100)
#     description = CharField(max_length=200, null=True)
#     body = TextField()
#     category = EnumField(EmailCategory, index=True)

#     class Meta:
#         table_name = "raven_concepts"


# class BulkEmail(WiLoModel):
#     email_category = EnumField(EmailCategory)
#     subject = CharField(max_length=200)
#     body = TextField()
#     created = DateTimeField(default=datetime.now)
#     updated = DateTimeField(null=True)
#     status = EnumField(MailStatus, default=MailStatus.PENDING)

#     class Meta:
#         table_name = "raven_bulk_emails"


# class AuditLog(WiLoModel):
#     bulk_email = ForeignKeyField(
#         BulkEmail, backref="email_audit_logs", on_delete="CASCADE"
#     )
#     customer_name = CharField(max_length=100)
#     customer_email = CharField(max_length=255)
#     status = EnumField(MailStatus, default=MailStatus.PENDING)

#     class Meta:
#         table_name = "raven_audit_logs"


# ======================================================================
# Model Maps
# ======================================================================
# class CustomerLabel(WiLoModel):
#     customer = ForeignKeyField(Customer, on_delete="CASCADE", backref="customer_labels")
#     label = ForeignKeyField(Label, on_delete="CASCADE", backref="label_customers")

#     class Meta:
#         table_name = "raven_map_customers_labels"
#         indexes = (
#             # Specify a unique multi-column index
#             (("customer", "label"), True),
#         )


# class ConceptLabel(WiLoModel):
#     concept = ForeignKeyField(Concept, on_delete="CASCADE", backref="concept_labels")
#     label = ForeignKeyField(Label, on_delete="CASCADE", backref="label_concepts")

#     class Meta:
#         table_name = "raven_map_concepts_labels"
#         indexes = (
#             # Specify a unique multi-column index
#             (("concept", "label"), True),
#         )


# class BulkEmailLabel(WiLoModel):
#     bulk_email = ForeignKeyField(
#         BulkEmail, on_delete="CASCADE", backref="bulk_email_labels"
#     )
#     label = ForeignKeyField(Label, on_delete="CASCADE", backref="label_bulk_emails")

#     class Meta:
#         table_name = "raven_map_bulk_emails_labels"
#         indexes = (
#             # Specify a unique multi-column index
#             (("bulk_email", "label"), True),
#         )
