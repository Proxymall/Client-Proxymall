from fastapi.encoders import jsonable_encoder
import uvicorn
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status
from typing import Optional
from datetime import datetime, timedelta, date
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from typing import List
from fastapi.params import Body

from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
# from .routers import entreprises, consultants
from app import crud
from app import models, schemas, database
from app.database import db_state_default

from authlib.integrations.starlette_client import OAuth
from starlette.config import Config


database.db.connect()
database.db.create_tables([
    models.User,
    models.Category,
    models.Order,
    models.Boutique,
    models.TypeUser,
    # models.Projet.intervenants.get_through_model()
])
database.db.close()

app = FastAPI(
    title="ProxyMall API",
    version="0.1",
    description="Api concu Pour servir de backend au projet ProxyMall",
    debug=True
)
app.add_middleware(SessionMiddleware, secret_key="secret-string")


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "69b78afe31586617945d1560c6036bbc9f5c5544b96d96215d144cf6195b195c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

# ============== Dependency start ============== #
async def reset_db_state():
    database.db._state._state.set(db_state_default.copy())
    database.db._state.reset()


# Dependency
def get_db(db_state=Depends(reset_db_state)):
    try:
        database.db.connect()
        yield
    finally:
        if not database.db.is_closed():
            database.db.close()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):  # password verif
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):  # Hasher le mot de passe
    return pwd_context.hash(password)


def get_user(username: str):
    db_user = crud.get_user_by_username(username)
    print(db_user)
    if username in db_user.username:
        # user_dict = db_user[username]
        # return models.User(**user_dict)
        # return models.User(**db_user)
        return db_user


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# recuperer un User grace a son Token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if not current_user.isactive:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# ============== Dependency end ============== #

# Route methods start
@app.get("/", tags=["Doc"])
def main():
    return RedirectResponse(url="/docs/")


@app.get("/doc2", tags=["Doc"])
def main():
    return RedirectResponse(url="/redoc/")
# =============== Google auth =============== #
config = Config('.env')  # read config from .env file
oauth = OAuth(config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@app.get('/login')
async def login(request: Request):
    # absolute url for callback
    # we will define it below
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)
    
@app.get('/auth')
async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = await oauth.google.parse_id_token(request, token)
    return user
# =============== Google auth =============== #



# =============== generate Token =============== #
@app.post("/token", response_model=Token, tags=["User"], dependencies=[Depends(get_db)])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(
        form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "Bearer", "user":user}
# =============== generate token =============== #


# ============== User start ============== #
@app.post("/users/", response_model=schemas.User, tags=["User"], dependencies=[Depends(get_db)])
async def create_user(user: schemas.UserBase = Body(..., embed=True)):
    db_user = crud.get_user_by_email(email=user.email)
    db_user1 = crud.get_user_by_username(username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Cet Email existe deja")
    if db_user1:
        raise HTTPException(
            status_code=400, detail="Ce nom d'utilisateur existe deja")
    return crud.create_user(user=user)


@app.get("/users/me/", response_model=schemas.User, tags=["User"], dependencies=[Depends(get_db)])
async def read_users_me(current_user: schemas.UserBase = Depends(get_current_active_user)):
    return current_user


@app.get("/users/", response_model=List[schemas.User], tags=["User"], dependencies=[Depends(get_db), Depends(get_current_active_user)])
def read_users(skip: int = 0, limit: int = 100 ):
# def read_users(skip: int = 0, limit: int = 100 , auth_user: schemas.User = Depends(get_current_active_user)):
    users = crud.get_users(skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User, tags=["User"], dependencies=[Depends(get_db)])
def read_user(user_id: int):
    db_user = crud.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/users/{id}", response_model=schemas.User, tags=["User"], dependencies=[Depends(get_db)])
def update_users(id: int, user: schemas.UserUpdate):
    """
    Supporte la mise a jour partiel. C'est a dire que vous n'etes pas obligé de renseigner tout les champs.
    Mettez a jour juste les données a modifier et ignorer les autres va parfaitement marcher
    """
    stored_data = jsonable_encoder(crud.get_user(id))
    if stored_data is None:
        raise HTTPException(status_code=404, detail="User not found")
    sotred_model = schemas.UserUpdate(**stored_data["__data__"])
    updated_data = user.dict(
        exclude_unset=True, exclude_none=True, exclude_defaults=True)
    updated_user = sotred_model.copy(update=updated_data)
    return crud.update_user(id, updated_user)
# ============== User end ============== #


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# uvicorn main:app --host 0.0.0.0 --port 80
