import functools

from flask import (
    
    Blueprint, flash,g, render_template, request, url_for, session
    # flash= nos permite enviar mensajes de manera generica a nuestras
    #plantillas.
    # Blueprint: Agrupacion de modulos que hacen sentido
)

from werkzeug.security import check_password_hash, generate_password_hash
# check_password_hash: verificar if password==other_password
# generate_password_hash: encripar password

from todo.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.app.route('/register', method=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None
        c.execute(
            'select id from user where username = %s'
        )
        if not username:
            error = 'Username es requerido'
        if not password:
            error = 'Password es requerido'
        elif c.fetchone() is not None:
            error = 'Usuario {} se encuentra registrado.'.format(username)

        if error is None:
            c.execute(
                'insert into user (username, password) values (%s, %s)'
                (username, generate_password_hash(password))
            )
            db.commit()

            return redirect(url_for('auth.login'))
    
        flash(error)
    
    return render_template('auth/register.html')
