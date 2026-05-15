import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1IiwiZXhwIjoxNzc5NDQ5MTkwfQ.VA1sTJBEgON9mr0ArkQtOYtDd3tpqkcaNTdGOt81U1Q"  
}

requisicao = requests.get(url="http://127.0.0.1:8000/auth/refresh", headers= headers)    
print(requisicao)
print(requisicao.json())
