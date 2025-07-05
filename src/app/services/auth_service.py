from src.app.clients.dummyjson_client import post_dummyjson_login

def user_login(username: str, password: str):
    return post_dummyjson_login(username, password)