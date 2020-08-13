from flask_app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False, nullable=False)
    name = db.Column(db.String, unique=False, nullable=False)
    all_cases = db.Column(db.Integer, unique=False, nullable=False)
    army = db.Column(db.Integer, unique=False, nullable=False)
    prohibited = db.Column(db.Integer, unique=False, nullable=False)
    classified = db.Column(db.Integer, unique=False, nullable=False)
    secret = db.Column(db.Integer, unique=False, nullable=False)
    сontraband = db.Column(db.Integer, unique=False, nullable=False)


    @staticmethod
    def add_new_user(name, user_id):
        user = User(name=name, user_id=user_id, сontraband=0, all_cases=0,
                    army=0, prohibited=0, classified=0, secret=0)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_user(user_id):
        user = db.session.query(User).filter_by(user_id=user_id).first()
        return user

    @staticmethod
    def update_quality(user, quality):
        user.all_cases += 1
        if quality == 'contraband':
            user.contraband += 1
        elif quality == 'secret':
            user.secret += 1
        elif quality == 'classified':
            user.classified += 1
        elif quality == 'prohibited':
            user.prohibited += 1
        else:
            user.army += 1

        db.session.commit()

    @staticmethod
    def get_top():
        return db.session.query(User).order_by(User.сontraband).all()[::-1]

    @staticmethod
    def get_statistics(user):
        return user.all_cases, user.сontraband, user.secret, user.classified, user.prohibited, user.army


if __name__ == '__main__':
    db.create_all()
