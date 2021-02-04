from fastapi.encoders import jsonable_encoder
from app import main
from sqlalchemy.orm import Session

from app import models, schemas
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ================ TypeUser start ================ #
def get_type_user(type_user_id: int):
    return models.TypeUser.filter(models.TypeUser.id == type_user_id).first()


def get_type_users(skip: int = 0, limit: int = 100):
    return list(models.TypeUser.select().offset(skip).limit(limit))


def create_type_user(type_user: schemas.TypeUserBase):
    db_type_user = models.TypeUser(**type_user.dict())
    db_type_user.save()
    return db_type_user

def delete_type_user(type_user_id):
    n = models.TypeUser.delete_by_id(type_user_id)
    if (n>0):
        return {"status": 200, "detail": "Suppression effectuée"}
    return {"status": 500, "detail": "Aucune suppression n'a été effectuée"}
# ================ TypeUser start ================ #



# ================ User start ================ #
def get_user(user_id: int):
    return models.User.filter(models.User.id == user_id).first()
    # return models.User.filter(models.User.id == user_id).first()


def get_user_by_email(email: str):
    return models.User.filter(models.User.email == email).first()

def get_user_by_username(username: str):
    return models.User.filter(models.User.username == username).first()


def get_users(skip: int = 0, limit: int = 100):
    return list(models.User.select().offset(skip).limit(limit))
    # return models.User.select().offset(skip).limit(limit)


def create_user(user: schemas.UserBase):
    password = pwd_context.hash(user.password)

    db_user = models.User(
        first_name = user.first_name,
        last_name = user.last_name,
        username = user.username,
        email = user.email,
        hashed_password=password,
        column=user.column,
        isactive=True,
        typeuser_id = user.typeuser_id
    )
    db_user.save()
    return db_user


def update_user(user_id: int, db_user: schemas.UserUpdate):
    # saved = jsonable_encoder(get_user(user_id))
    # print(saved['__data__']['hashed_password'])
    # # saved['__data__']['hashed_password']
    # if (main.verify_password(plain_password=db_user.password, hashed_password=saved['__data__']['hashed_password'])):
    #     return {"status":500, "detail":"Votre nouveau mot de passe est identique a l'ancien"}
    # else:
    # password = pwd_context.hash(db_user.password)
    q = (models.User.update({
        models.User.first_name: db_user.first_name,
        models.User.last_name: db_user.last_name,
        models.User.email: db_user.email,
        models.User.address: db_user.address,
        models.User.typeuser_id: db_user.typeuser_id,
        models.User.username: db_user.username,
        # models.User.hashed_password: password,
        models.User.column: db_user.username,
        models.User.isactive: db_user.isactive,
    }).where(models.User.id == user_id))
    nb_row = q.execute()
    return get_user(user_id)


def delete_user(user_id):
    n = models.User.delete_by_id(user_id)
    if (n>0):
        return {"status": 200, "detail": "Suppression effectuée"}
    return {"status": 500, "detail": "Aucune suppression n'a été effectuée"}
# ================ User start ================ #



# ================ Category start ================ #
def get_category(category_id: int):
    return models.Category.filter(models.User.id == category_id).first()


def get_categories(skip: int = 0, limit: int = 100):
    return list(models.Category.select().offset(skip).limit(limit))


def create_category(category: schemas.CategoryBase):
    db_category = models.Category(
        title = category.title,
        description = category.description
    )
    db_category.save()
    return db_category

def delete_category(category_id):
    n = models.Category.delete_by_id(category_id)
    if (n>0):
        return {"status": 200, "detail": "Suppression effectuée"}
    return {"status": 500, "detail": "Aucune suppression n'a été effectuée"}
# # ================ Category start ================ #



# ================ Boutique start ================ #
def create_boutique(boutique: schemas.BoutiqueBase):
    db_boutique = models.TypeUser(
        name = boutique.name,
        slogan = boutique.slogan, 
        location = boutique.location,
        registration_date = boutique.registration_date,
        category_id = boutique.category_id
    )
    db_boutique.save()
    return db_boutique


def create_user_boutique(boutique: schemas.BoutiqueBase, user_id: int):
    db_boutique = models.Boutique(**boutique.dict(), owner_id=user_id)
    db_boutique.save()
    return db_boutique


def get_boutique(boutique_id: int):
    return models.Boutique.filter(models.User.id == boutique_id).first()


def get_boutiques(skip: int = 0, limit: int = 100):
    return list(models.TypeUser.select().offset(skip).limit(limit))

def delete_boutique(boutique_id):
    n = models.Boutique.delete_by_id(boutique_id)
    if (n>0):
        return {"status": 200, "detail": "Suppression effectuée"}
    return {"status": 500, "detail": "Aucune suppression n'a été effectuée"}
# # ================ Boutique start ================ #

# def get_items(skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
