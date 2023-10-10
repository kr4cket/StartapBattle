from peewee import *
from core.db_conn import DBConnection


class BaseModel(Model):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        database = DBConnection().get_handle()


class Language(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=255, unique=True)


class Theme(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=255, unique=True)


class LanguageLevel(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=255)
    lang = ForeignKeyField(Language, backref="langs")


