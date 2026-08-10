"""
This file will oversee getting data from the database
Two tables will exist; one for the email body and one for the group orchestration
-> 1: Group ID, Name, Header, Body, Image / Image URL
-> 2: Group ID, [email, name]
"""

from pydantic import BaseModel, ConfigDict, ValidationError, Field
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from typing_extensions import Annotated
from datetime import datetime

# ===================
#  JSON SCHEMA
# ===================

class GroupMember(BaseModel):
    email: str
    name: str

class Group(BaseModel):
    group_id: str
    group_members: list[GroupMember] = Field(default_factory=list)

class BlogBody(BaseModel):
    group_id: str
    name: str
    header: str
    body: str
    image: str
    month: Annotated[int, Field(ge=1, le=12)]

# ===================
#  MONGO SETUP
# ===================

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")

if not MONGO_URI:
    raise ValueError("MONGODB_URI is not set")

MONGO_PASSWORD = os.getenv("MONGODB_PASSWORD")
MONGO_USERNAME = os.getenv("MONGODB_USERNAME")

client = MongoClient(MONGO_URI)
db = client.monthly_group_blog
groups_collection = db.groups
blog_body_collection = db.blog_body

# ===================
#  MONGO CRUD
# ===================

def get_current_month() -> int:
    dt_now = datetime.now()
    return dt_now.month

def read_group_and_blog_body(group_id: str) -> tuple[Group, list[BlogBody]]:
    month = get_current_month()

    group_doc = groups_collection.find_one({"group_id": group_id})
    if not group_doc:
        raise ValueError(f"Group with ID {group_id} not found")

    blog_docs = list(blog_body_collection.find({"group_id": group_id, "month": month}))
    if not blog_docs:
        raise ValueError(...)

    group_doc.pop("_id", None)

    all_blogs: list[BlogBody] = []

    for blog in blog_docs:
        blog.pop("_id", None)
        all_blogs.append(BlogBody.model_validate(blog))

    return Group.model_validate(group_doc), all_blogs

def insert_member_to_group(group_id: str, member_email: str, member_name: str) -> None:
    member = GroupMember(email=member_email, name=member_name)
    groups_collection.update_one(
        {"group_id": group_id},
        {"$addToSet": {"group_members": member.model_dump()}},
        upsert=True
    )

def insert_blog_body(group_id: str, name: str, header: str, body: str, image: str) -> None:
    month = get_current_month()

    blog = BlogBody(group_id=group_id, name=name, header=header, body=body, image=image, month=month)
    blog_body_collection.update_one(
        {"group_id": group_id, "month": month},
        {"$set": blog.model_dump()},
        upsert=True
    )

