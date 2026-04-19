from django.test import TestCase
import requests
# Create your tests here.


r = requests.get('http://localhost:8000/music/listen/1')

print(r.headers['Content-Type'])