from flask import *
from database import *

admin=Blueprint('admin',__name__)

@admin.route('/admin')
def adminhome():
    return render_template('admin_home.html')

