from main import app
from flaskext.mysql import MySQL

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'fastapp'
app.config['MYSQL_DATABASE_PASSWORD'] = '2GyXg4juY3gJYWK'
app.config['MYSQL_DATABASE_DB'] = 'fast'
app.config['MYSQL_DATABASE_HOST'] = 'fastapp.mysql.pythonanywhere-services.com'
mysql.init_app(app)
