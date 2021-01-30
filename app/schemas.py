from typing import List, Optional, Any
from datetime import datetime, date
from pydantic import BaseModel
from datetime import datetime, time, date, timedelta
from peewee import ModelSelect
from pydantic.utils import GetterDict


class PeeweeGetterDict(GetterDict):  # Necessaire seulement quand peewee est utilisé
    """ Permet a Peewee de pouvoir gerer les données de type `list()` et `List[]` """

    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)
        return res


class CategoryBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class BoutiqueBase(BaseModel):
    name: Optional[str] = None
    slogan: Optional[str] = None
    location: Optional[str] = None
    registration_date: Optional[date] = None
    category_id: Optional[int] = None

class TypeUserBase(BaseModel):
    libelle: Optional[str] = None
    

class UserBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None 
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    address: Optional[str] = None
    column: Optional[str] = None


class TypeUser(TypeUserBase):
    id: Optional[int] = None
    isactive: Optional[bool] = None
    class Config:
        
        getter_dict = PeeweeGetterDict
        getter_dict = PeeweeGetterDict
 

class Category(CategoryBase):
    id: Optional[int] = None
    parent_id: Optional[int] = None
    class Config:
        
        getter_dict = PeeweeGetterDict



class User(BaseModel):
    id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None 
    username: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    column: Optional[str] = None
    isactive: Optional[bool] = None
    type_user_id: Optional[int] = None
    type_user: Optional[TypeUser] = None
    class Config:
        
        getter_dict = PeeweeGetterDict


class Boutique(BoutiqueBase):
    id: Optional[int] = None
    category: Optional[Category] = None
    owner: Optional[User] = None

    class Config:
        
        getter_dict = PeeweeGetterDict