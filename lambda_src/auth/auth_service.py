import xmlrpc.client
from ssl import SSLCertVerificationError
from .auth_schema import AuthDto
from ..config import settings
from ..common.enums import ApiResponseMessage

async def authenticate():
    # Connect to Odoo
    odoo = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(settings.url))
    try:
        uid = odoo.authenticate(
            settings.database_name, settings.username, settings.password, {}
        )

        if(uid == False):
            return {"success": False, "error": "Authentication failed"}

        return str(uid)
    except SSLCertVerificationError as connectionError:
        return {"success": False, "error": f"SSL error: {connectionError.reason}"}