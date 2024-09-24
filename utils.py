import os


def get_google_api_key() -> str:
    key = os.environ.get('GOOGLE_API_KEY', None)
    if key is None:
        return input("Insert Google API key:")
    else:
        return key
