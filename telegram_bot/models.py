from sqlalchemy import Column, Integer, String, Text
from db import Base


class WebUserForm(Base):
    __tablename__ = 'web_user_form'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), index=True)
    email = Column(String(150), nullable=True)
    type_appeal = Column(String(150), nullable=True)
    message = Column(Text, nullable=True)
    status = Column(String(20), nullable=True)