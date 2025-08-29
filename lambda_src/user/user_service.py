import xmlrpc.client
from typing import List
from .user_schema import User
from ..config import settings
from ..common.schema import Lead
import ssl
from ..auth.auth_service import authenticate


def save(lead: Lead, uid: str) -> str:
    context = ssl._create_unverified_context()
    odoo = xmlrpc.client.ServerProxy(
        "{}/xmlrpc/2/object".format(settings.url), context=context
    )
    id = odoo.execute_kw(
        settings.database_name,
        uid,
        settings.password,
        "res.partner",
        "create",
        [{"email": lead.email, "phone": lead.phone, "name": lead.name}],
    )
    return str(id)


def update(id: int, lead: Lead, uid: str) -> None:
    context = ssl._create_unverified_context()
    odoo = xmlrpc.client.ServerProxy(
        "{}/xmlrpc/2/object".format(settings.url), context=context
    )
    odoo.execute_kw(
        settings.database_name,
        uid,
        settings.password,
        "res.partner",
        "write",
        [[id]],
        [{"email": lead.email, "phone": lead.phone}],
    )


def getAll(offset: int, limit: int):
    uid = authenticate()

    # Connect to Odoo
    odoo = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(settings.url))
    search_domain = [[]]
    user_ids = odoo.execute_kw(
        settings.database_name,
        uid,
        settings.password,
        "res.partner",
        "search",
        search_domain,
        {"offset": offset, "limit": limit},
    )
    records = odoo.execute_kw(
        settings.database_name,
        uid,
        settings.password,
        "res.partner",
        "read",
        [user_ids],
        {"fields": ["name", "email", "phone"]},
    )
    return records


def getByPhoneNumber(phone_number: str, uid: str) -> List[User]:
    context = ssl._create_unverified_context()
    odoo = xmlrpc.client.ServerProxy(
        "{}/xmlrpc/2/object".format(settings.url), context=context
    )
    search_domain = [[["phone", "=", phone_number]]]
    records = odoo.execute_kw(
        settings.database_name,
        uid,
        settings.password,
        "res.partner",
        "search_read",
        search_domain,
        {"fields": ["email", "phone", "name"], "limit": 1},
    )

    if not records or not isinstance(records, list):
        return []

    return [User.model_validate(r) for r in records]


def getByEmail(email: str, uid: str) -> List[User]:
    context = ssl._create_unverified_context()
    odoo = xmlrpc.client.ServerProxy(
        "{}/xmlrpc/2/object".format(settings.url), context=context
    )
    search_domain = [[["email", "=", email]]]
    records = odoo.execute_kw(
        settings.database_name,
        uid,
        settings.password,
        "res.partner",
        "search_read",
        search_domain,
        {"fields": ["email", "phone", "name"], "limit": 1},
    )

    if not records or not isinstance(records, list):
        return []

    user_emails = [User.model_validate(r) for r in records]
    return user_emails
