from tags.database import db


class Tags(db.Document):
    email = db.EmailField(required=True, unique=True)
    tags = db.ListField()



