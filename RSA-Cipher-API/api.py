from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from http import HTTPStatus
import secrets

from cipher import RSA_Logic

app = FastAPI()
security = HTTPBasic()

'''
Cipher parameters
'''
public, private = RSA_Logic.generate_keys()

'''
API models
'''

ciph_db = []

users_db = [{'username': 'hubertkniola',
             'password': 'password'}, ]


class CiphItem(BaseModel):
    message: str
    encrypted: str
    decrypted: str


class SingleMessage(BaseModel):
    message: str


'''
API's authentication 
'''

for i, val in enumerate(ciph_db):
    print(i)
    print(val)


def get_current_user(cred: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(cred.username, "hubertkniola")
    correct_password = secrets.compare_digest(cred.password, "password")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return cred.username


@app.get("/user")
def read_current_user(username: str = Depends(get_current_user)):
    return {"username": username}


'''
Simple basic endpoints with implemented methods
'''


@app.post('/allinone')
async def allinone(ciph: CiphItem):
    temp_enc = RSA_Logic.encode(ciph.message, public)
    temp_dec = RSA_Logic.decode(temp_enc, private)
    element = {'message': ciph.message, 'encrypted': temp_enc, 'decrypted': temp_dec}
    ciph_db.append(element)
    return {'message': ciph.message, 'encrypted': temp_enc, 'decrypted': temp_dec}


@app.get('/elements')
async def elements():
    return ciph_db


@app.post('/element/{id}')
async def element(id: int):
    return ciph_db[id]


@app.post('/encode')
async def encode(mess: SingleMessage):
    return {'message': f'Encrypted message: {RSA_Logic.encode(mess.message, public)}'}


@app.post('/decode')
async def decode(mess: SingleMessage):
    return {'message': f'Decrypted message: {RSA_Logic.decode(mess.message, private)}'}
