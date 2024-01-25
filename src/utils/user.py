import jwt
import os
from dotenv import load_dotenv
from utils.responses import error, success

load_dotenv()

def parse_token(token):
    try:
        return jwt.decode(token.encode("utf-8"), key=os.getenv("JWT_SECRET"), algorithms=["HS256"])
    except Exception as e: 
        print(e)
        return False
    

class User:
    def __init__(self, token):
        self.token = token
        # parse token
        self.id = parse_token(token).id
        self.get_user()
    
    def get_user():
        cursor = db.connect().cursor()
        cursor.execute(f"SELECT * FROM Users WHERE UserID={self.id}")
        res = cursor.fetchone()
        if res is None: 
            self.exists = error(401, "User does not exist.")
            
        else: self.exists = True
        (_, self.house_id, self.username, self.password_hash) = res
        
    def login(username, password):
        if self.username != username: return error(401, "Incorrect username or password.")
        if not bcrypt.checkpw(password, self.password_hash): return error(401, "Incorrect username or password.")
        token = jwt.encode(payload={"id": self.id}, key=os.getenv("JWT_SECRET"), algorithm="HS256")
        return success({
            "token": token,
            "user": {
                "id": self.id,
                "username": self.username,
                "house_id": self.house_id
            }
        })