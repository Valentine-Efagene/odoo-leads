import xmlrpc.client
from typing import List
from .user_schema import User
from ..config import settings
from ..common.schema import Lead
from ..auth.auth_service import authenticate

async def save(lead: Lead) -> str:
    uid = await authenticate()

    odoo = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(settings.url))
    id = odoo.execute_kw(
        settings.database_name, 
        uid, 
        settings.password, 
        'res.partner', 
        'create', 
        [{
            "email": lead.email,
            "phone": lead.phone
        }])
    return str(id)

async def update(id: int, lead: Lead) -> None:
    uid = await authenticate()

    odoo = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(settings.url))
    odoo.execute_kw(
        settings.database_name, 
        uid, 
        settings.password, 
        'res.partner', 
        'write',
        [[id]],
        [{
            "email": lead.email,
            "phone": lead.phone
        }])

async def getAll(offset: int, limit: int):
    uid = await authenticate()

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


async def getByPhoneNumber(phone_number: str) -> List[User]:
    uid = await authenticate()
    odoo = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(settings.url))
    search_domain = [[["phone", "=", phone_number]]]
    records = odoo.execute_kw(
        settings.database_name,
        uid,
        settings.password,
        "res.partner",
        "search_read",
        search_domain,
        {'fields': ['email'], 'limit': 1}
    )

    if not records or not isinstance(records, list):
        return []
    
    return [User.model_validate(r) for r in records]


async def getByEmail(email: str) -> List[User]:
    uid = await authenticate()
    odoo = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(settings.url))
    search_domain = [[["email", "=", email]]]
    records = odoo.execute_kw(
        settings.database_name,
        uid,
        settings.password,
        "res.partner",
        "search_read",
        search_domain,
        {'fields': ['email'], 'limit': 1}
    )

    if not records or not isinstance(records, list):
        return []

    user_emails = [User.model_validate(r) for r in records]
    return user_emails
