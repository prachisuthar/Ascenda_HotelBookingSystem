from django.apps import AppConfig
import requests
import requests_cache
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

requests_cache.install_cache('github_cache', backend='sqlite', expire_after=18000)


class EscappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'escapp'