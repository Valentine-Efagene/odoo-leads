import xmlrpc.client
from ..config import settings


def authenticate() -> str | None:
    odoo = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(settings.url))

    uid = odoo.authenticate(
        settings.database_name, settings.username, settings.password, {}
    )

    if uid == False:
        return None

    return str(uid)
