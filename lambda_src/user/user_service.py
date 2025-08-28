import xmlrpc.client
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


async def getByPhoneNumber(phone_number: str) -> str:
    # Connect to Odoo
    uid = await authenticate()

    odoo = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(settings.url))
    search_domain = [[["phone", "=", phone_number]]]
    user_ids = odoo.execute_kw(
        settings.database_name,
        uid,
        settings.password,
        "res.partner",
        "search",
        search_domain,
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
    return str(records)


async def getByEmail(email: str) -> str:
    # Connect to Odoo

    uid = await authenticate()

    odoo = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(settings.url))
    search_domain = [[["email", "=", email]]]
    user_ids = odoo.execute_kw(
        settings.database_name,
        uid,
        settings.password,
        "res.partner",
        "search",
        search_domain,
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
    return str(records)
