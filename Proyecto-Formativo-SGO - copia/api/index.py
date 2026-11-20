"""Entrypoint WSGI para Vercel. Vercel busca la variable `app`."""
from app import create_app

app = create_app()