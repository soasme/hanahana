from flask import url_for, session, request, redirect
from .core import spa
from hana.core import db
from hana.auth.app import require_auth, current_user
from hana.auth.models import User
from hana.hana.models import Hana

def _render_template(body):
    me = f'<a href=\'{url_for(".user_home", username=current_user.username)}\'>{current_user.username}</a> | <a href=\'{url_for("auth.logout")}\'>logout</a>'
    _body = f'<h1><a style="text-decoration:none;" href=\'{url_for(".index")}\'>🌸 Hana</a></h1><p>login as {me}<p><div>{body}</div>'
    return f'<html><body>{_body}</body></html>'

@spa.route('/readme')
def readme():
    body = f'<a href=\'{url_for("auth.login")}\'>login</a>'
    return f'<html><body>{body}</body></html>'

@spa.route('/')
def index():
    if not session.get('sid'):
        return redirect(url_for('.readme'))

    from hana.auth.models import User
    users = User.query.all()
    urls = ' | '.join([
        f'<a href=\'{url_for(".user_home", username=user.username)}\'>{user.username}</a>'
        for user in users
    ])
    return _render_template(urls)

@spa.route('/u/<username>', methods=['GET', 'POST'])
@require_auth
def user_home(username):
    remark = ''
    user = User.query.filter_by(username=username).first()

    if request.method == 'POST':
        remark = request.form['remark']
        is_private = int(request.form['is_private'])
        hana = Hana(from_id=session['sid'], to_id=user.id, remark=remark, is_private=is_private)
        db.session.add(hana)
        db.session.commit()
        return redirect(url_for(".user_home", username=username, success=1))
    form = """
    <form method="POST">
        <div>
            <input type="radio" name="is_private" value="0" id="public">
            <label for="public">Public</label>
            <input type="radio" checked name="is_private" value="1" id="private">
            <label for="private">Private</label>
        </div>
        <div>
        <label for="remark">Remark</label>
        <textarea name="remark" id="remark">%(remark)s</textarea>
        </div>
        <input type=submit value="Give him/her a hana 🌸">
    </form>
    """ % dict(remark=remark)
    hint = "<p>You just gave him a hana 🌸 !</p>" if 'success' in request.args else ""

    hanas = Hana.query.filter_by(to_id=user.id).order_by(Hana.created_at.desc()).all()
    user_ids = {hana.from_id for hana in hanas}
    users = {id: User.query.get(id) for id in user_ids}
    hanas = ''.join([
        f'<div><a href=\'{url_for(".user_home", username=users[hana.from_id].username)}\'>{users[hana.from_id].username}</a><br>🌸 {hana.remark}<br>{hana.created_at}</div>'
        for hana in hanas
    ])
    html = hint + (form if session['sid'] != user.id else '') + hanas
    return _render_template(html)
