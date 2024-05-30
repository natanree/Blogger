from app import create_app, db
from app.Model.models import User, Post, Tag
import sys

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': app.db, 'User':User}

@app.before_request
def initDB(*args,**kwargs):
    if app._got_first_request:
        db.create_all()
        if Tag.query.count() == 0:
            tags = ['tech', 'diary']
            for tag in tags:
                theTag = Tag(name=tag)
                db.session.add(theTag)
            db.session.commit()
        if User.query.count() == 0:
            user = User(username = 'test', first_name = 'John', last_name = 'Doe', email = 'test@gmail.com')
            user.set_password('123')
            user.set_verification('ifawvcKvBd')
            user.preferred_tags.append(Tag.query.filter_by(id = 1).first())
            db.session.add(user)
            db.session.commit()
        
if __name__ == "__main__":
    app.run(debug=True)