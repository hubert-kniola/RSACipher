from fastapi import Depends, FastAPI, HTTPException, status
from pydantic.class_validators import Optional
from cipher import RSA_Logic
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()
security = HTTPBasic()

public, private = RSA_Logic.generate_keys()

users_db = {
    "hubertkniola": {
        "username": "hubertkniola",
        "full_name": "Hubert Knioła",
        "email": "hubert_kniola@gmail.com",
        "hashed_password": "password",
        "disabled": False,
    },
}


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Security

@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}


def password_hasher(password: str):
    return RSA_Logic.encode(password, public)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


class UserInDB(User):
    hashed_password: str


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = decode_token(token)
    return user


async def get_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = password_hasher(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


# Others

@app.post('/encode/{to_encrypt}')
async def encode(to_encrypt: str):
    return {'message': f'Encrypted message: {RSA_Logic.encode(to_encrypt, public)}'}


@app.post('/decode/{to_decode}')
async def decode(to_decode: str):
    return {'message': f'Encrypted message: {RSA_Logic.decode(to_decode, private)}'}

