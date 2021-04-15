from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from pywin.dialogs import status

from cipher import RSA_Logic
from passlib.context import CryptContext

app = FastAPI()  # API's instance
security = HTTPBasic()  # Security instance

'''
Cipher parameters
'''
public, private = RSA_Logic.generate_keys()  # RSA keys generator
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # password hash method

'''
API models
'''

ciph_db = []  # Basic database used to encoding and decoding

users_db = {  # Basic database with one user used to authentication
    "hubertkniola": {
        "username": "hubertkniola",
        "hashed_password": "$2b$12$z0crAbk1cJtTL7MRm55mXuPnLGteTdKSfVEwWouasQNQtvmNOACcu", # 'password' in hash
        "disabled": False,
    }
}


class CiphItem(BaseModel):  # Cipher model
    message: str
    encrypted: str
    decrypted: str


class SingleMessage(BaseModel):  # Message model
    message: str


class User(BaseModel):  # User model
    username: str
    disabled: bool = None


class UserInDB(User):  # User's password model
    hashed_password: str


'''
API's authentication 
'''


def get_user(db, username: str):  # Function to get user from database
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def get_password_hash(password):  # Function to hash gives password
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):  # Function to verify gives password
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(fake_db, username: str, password: str):  # Function to authenticate user with database
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):  # Function to simple authentication
    user = authenticate_user(users_db, credentials.username, credentials.password)
    if not user:
        raise HTTPException(  # Raise exception after check thas user does not exist
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/example")   # Endpoint used to get name of the current user
def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}


'''
Simple basic endpoints with implemented methods
'''


@app.get("/")  # Root endpoint
async def root():
    return {"message": "Hello World"}


@app.post('/allinone')  # Endpoint with encode and decode methods
async def allinone(ciph: CiphItem):
    temp_enc = RSA_Logic.encode(ciph.message, public)
    temp_dec = RSA_Logic.decode(temp_enc, private)
    element = {'message': ciph.message, 'encrypted': temp_enc, 'decrypted': temp_dec}
    ciph_db.append(element)
    return {'message': ciph.message, 'encrypted': temp_enc, 'decrypted': temp_dec}


@app.get('/elements')  # Endpoint to get all of stored items
async def elements():
    return ciph_db


@app.post('/element/{id}')  # Endpoint to get one of storeditems
async def element(id: int):
    return ciph_db[id]


@app.post('/encode')  # Endpoint to encode gives message
async def encode(mess: SingleMessage):
    return {'message': f'Encrypted message: {RSA_Logic.encode(mess.message, public)}'}


@app.post('/decode')  # Endpoint to decode gives message
async def decode(mess: SingleMessage):
    return {'message': f'Decrypted message: {RSA_Logic.decode(mess.message, private)}'}
