from sqlalchemy.orm import Session

from app import models, schemas
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ================ TypeUser start ================ #
def get_type_user(db: Session, type_user_id: int):
    return db.query(models.TypeUser).filter(models.User.id == type_user_id).first()


def get_type_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TypeUser).offset(skip).limit(limit).all()


def create_type_user(db: Session, type_user: schemas.TypeUserBase):
    db_type_user = models.TypeUser(libelle= type_user.libelle)
    db.add(db_type_user)
    db.commit()
    db.refresh(db_type_user)
    return db_type_user

def delete_type_user(db: Session, type_user_id):
    db_type_user = get_type_user(db, type_user_id)
    db.delete(db_type_user)
    db.commit()
    return {"status": 200, "detail": "Suppression effectuée"}
# # ================ TypeUser start ================ #



# ================ User start ================ #
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserBase):
    password = pwd_context.hash(user.password)

    db_user = models.User(
        first_name = user.first_name,
        last_name = user.last_name,
        username = user.username,
        email = user.email,
        hashed_password=password,
        column=user.column
    )
    db.add(db_user)
    db.commit() 
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id):
    db_user = get_user(db, user_id)
    db.delete(db_user)
    db.commit()
    return {"status": 200, "detail": "Suppression effectuée"}
# ================ User start ================ #



# ================ Category start ================ #
def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.User.id == category_id).first()


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()


def create_category(db: Session, category: schemas.CategoryBase):
    db_category = models.Category(
        title = category.title,
        description = category.description
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id):
    db_category = get_category(db, category_id)
    db.delete(db_category)
    db.commit()
    return {"status": 200, "detail": "Suppression effectuée"}
# # ================ Category start ================ #



# ================ Boutique start ================ #
def create_boutique(db: Session, boutique: schemas.UserBase):
    fake_hashed_password = boutique.password + "notreallyhashed"
    db_boutique = models.TypeUser(
        name = boutique.name,
        slogan = boutique.slogan, 
        location = boutique.location,
        registration_date = boutique.registration_date,
        category_id = boutique.category_id
    )
    db.add(db_boutique)
    db.commit()
    db.refresh(db_boutique)
    return db_boutique


def create_user_boutique(db: Session, boutique: schemas.BoutiqueBase, user_id: int):
    db_boutique = models.Boutique(**boutique.dict(), owner_id=user_id)
    db.add(db_boutique)
    db.commit()
    db.refresh(db_boutique)
    return db_boutique


def get_boutique(db: Session, boutique_id: int):
    return db.query(models.TypeUser).filter(models.User.id == boutique_id).first()


def get_boutiques(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TypeUser).offset(skip).limit(limit).all()

def delete_boutique(db: Session, boutique_id):
    db_boutique = get_boutique(db, boutique_id)
    db.delete(db_boutique)
    db.commit()
    return {"status": 200, "detail": "Suppression effectuée"}
# # ================ Boutique start ================ #

# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
