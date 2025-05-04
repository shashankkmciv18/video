import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SECRETS_DIR = os.path.join(PROJECT_ROOT, 'secrets')
CLIENT_SECRETS_FILE = os.path.join(SECRETS_DIR, 'client_secrets.json')
TOKEN_FILE = os.path.join(SECRETS_DIR, 'token.json')
TOKEN_PICKLE_FILE = os.path.join(SECRETS_DIR, 'token.pickle')
