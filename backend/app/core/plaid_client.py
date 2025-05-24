from plaid import Configuration, ApiClient
from plaid.api import plaid_api
from .config import settings

def get_plaid_client() -> plaid_api.PlaidApi:
    host_map = {
        "sandbox": "https://sandbox.plaid.com",
        "development": "https://development.plaid.com",
        "production": "https://production.plaid.com",
    }
    configuration = Configuration(
        host=host_map[settings.plaid_env],
        api_key={
            "clientId": settings.plaid_client_id,
            "secret":    settings.plaid_secret,
            "plaidVersion": "2020-09-14",
        },
    )
    return plaid_api.PlaidApi(ApiClient(configuration))

# Optional: create one global so you don’t rebuild it every request
plaid_client = get_plaid_client()
