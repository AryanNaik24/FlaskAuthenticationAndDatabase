from website import create_app
from flask import url_for

#stores the returned value from create_app
app = create_app()


#runs only if we run the file 
if __name__ == '__main__':
    app.run(debug=True)