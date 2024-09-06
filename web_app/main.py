from website import create_app
from website import db_helper

# define app variable with create_app function
app = create_app()

# define database variable with db_helper class
db = db_helper()

# run db_helper functions to check for database structure
db.create_database()
db.create_tables()
db.create_daterange()

# run app if opened from main.py
if __name__ == '__main__':
    app.run(debug=True,)

    # use_reloader=False