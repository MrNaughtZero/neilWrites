from app.database import db
import hashlib
from hashlib import sha256
from sqlalchemy import desc

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    def get_id(self):
        return self.id
    
    def is_authenticated(self):
        return True

    def get_username(self):
        return self.username

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def create_user(self):
        self.password = self.hash_password(self.password)
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()

    @staticmethod
    def hash_password(password):
        return sha256(password.encode('utf-8')).hexdigest()

    def check_for_admin(self):
        return self.query.all()

    def login_attempt(self, username, password):
        query = self.query.filter_by(username=username, password=self.hash_password(password)).first() 
        if not query:
            return False
        return query

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    cat = db.Column(db.String(300), nullable=False)

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def check_category(self, name):
        return self.query.filter_by(cat=name).first()

    def return_category(self, id):
        return self.query.filter_by(id=id).first()

    def fetch_categories(self):
        return self.query.all()

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text(4294000000), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    last_update = db.Column(db.String(50), nullable=True)

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self, id):
        query = self.query.filter_by(id=id).first()
        db.session.delete(query)
        db.session.commit()
        
    def update(self, id, title, category, status, content, date):
        query = self.query.filter_by(id=id).first()
        query.title = title.replace(' ', '-')
        query.category = category
        query.status = status
        query.content = content
        query.last_updated = date
        db.session.commit()

    def all_posts(self):
        return self.query.order_by(desc(Post.id)).all()

    def custom_query(self, query, value):
        ''' custom user query. Pass through query, and value . example username:Ian '''
        return self.query.filter_by(**{query:value}).first()

    def posts_by_category(self, category):
        return self.query.filter_by(category=category).all()

    def last_submission(self):
        return self.query.order_by(desc(Post.id)).first()