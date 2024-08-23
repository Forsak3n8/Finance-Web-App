from website import create_app
from website import db_helper

app = create_app()

db = db_helper()

db.create_database()
db.create_tables()
db.create_daterange()

if __name__ == '__main__':
    app.run(debug=True,)

    # use_reloader=False