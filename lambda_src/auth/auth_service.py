import xmlrpc.client
import ssl
from ..config import settings


def authenticate() -> str | None:
    context = ssl._create_unverified_context()
    odoo = xmlrpc.client.ServerProxy(
        "{}/xmlrpc/2/common".format(settings.url), context=context
    )

    uid = odoo.authenticate(
        settings.database_name, settings.username, settings.password, {}
    )

    if uid == False:
        return None

    return str(uid)
