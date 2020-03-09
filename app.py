from flask import request, jsonify
from flask_cors import CORS

from backend.models.models import *
from config import *

DEBUG = True

CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/users', methods=["GET", "POST"])
def users():
    data_users = db.session.query(User).all()
    return jsonify({
        'data_users': [i.serialize for i in data_users]
    })


@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    answer = {'answer': 'error'}
    if request.method == 'POST':
        post_data = request.get_json()
        if post_data['user_name'] is not None:
            user = User(name=post_data['user_name'])
            name = user.name
            db.session.add(user)
            db.session.commit()
            role_employee_obj = Role.query.filter_by(
                name="employee").first()  # object Role with name employee
            added_user = User.query.filter_by(name=name).first()
            added_user._roles.append(role_employee_obj)
            db.session.commit()
            print(added_user)
            answer['added_user'] = added_user.serialize
            answer['answer'] = 'ok'
    return jsonify(answer)


@app.route("/update_user_name", methods=["POST"])
def update_user_name():
    answer = {'id': 0, 'answer': 'error'}
    if request.method == 'POST':
        post_data = request.get_json()
        user_id = post_data['id']
        new_user_name = post_data['user_name']
        user = db.session.query(User).filter_by(id=user_id).first()
        user.name = new_user_name
        db.session.commit()

        answer['answer'] = 'ok'

    return jsonify(answer)


@app.route("/delete_user", methods=["POST"])
def delete_user():
    answer = {'id': 0, 'answer': 'error'}
    if request.method == 'POST':
        post_data = request.get_json()
        user_id = post_data['id']
        user = db.session.query(User).filter_by(id=user_id).first()
        user._groups.clear()
        user._roles.clear()
        db.session.add(user)
        db.session.commit()
        db.session.delete(user)
        db.session.commit()
        answer['answer'] = 'ok'
    return jsonify(answer)


@app.route("/update_user_role", methods=["POST"])
def update_user_role():
    print("priveeeeT!")
    answer = {'id': 0, 'answer': 'error'}
    if request.method == 'POST':
        post_data = request.get_json()
        role_id = post_data['role_id']
        user_id = post_data['id']
        if role_id is None:
            answer['answer'] = 'role_id is None'
        else:
            main_user_id = db.session.query(User).get(user_id)
            main_role_id = db.session.query(Role).get(role_id)

            if main_role_id.name == "administrator":
                employee_object = Role.query.filter_by(name="employee").first()
                for obj in main_user_id._roles:
                    if obj == employee_object:
                        main_user_id._roles.remove(employee_object)
                        db.session.commit()
                        main_user_id._roles.append(main_role_id)
                        db.session.commit()
                        answer['answer'] = 'ok'
            elif main_role_id.name == "employee":
                admin_object = Role.query.filter_by(name="administrator").first()
                for obj in main_user_id._roles:
                    if obj == admin_object:
                        main_user_id._roles.remove(admin_object)
                        db.session.commit()
                        main_user_id._roles.append(main_role_id)
                        db.session.commit()
                        answer['answer'] = 'ok'
            else:
                main_user_id._roles.append(main_role_id)
                db.session.commit()
                answer['answer'] = 'ok'
        return jsonify(answer)


@app.route("/delete_user_role", methods=["POST"])
def delete_user_role():
    answer = {'id': 0, 'answer': 'error'}
    if request.method == 'POST':
        post_data = request.get_json()
        user_id = post_data['id']
        role_id = post_data['role_id']
        main_user_id = db.session.query(User).get(user_id)
        main_role_id = db.session.query(Role).get(role_id)

        if main_role_id.name == "employee":
            admin_object = Role.query.filter_by(name="administrator").first()
            for obj in main_role_id.users:
                if obj == main_user_id:
                    main_role_id.users.remove(main_user_id)
                    db.session.commit()
                    main_user_id._roles.append(admin_object)
                    db.session.commit()

        elif main_role_id.name == "administrator":
            employee_object = Role.query.filter_by(name="employee").first()
            for obj in main_role_id.users:
                if obj == main_user_id:
                    main_role_id.users.remove(main_user_id)
                    db.session.commit()
                    main_user_id._roles.append(employee_object)
                    db.session.commit()
        else:
            main_user_id._roles.remove(main_role_id)
            db.session.commit()

        answer['answer'] = 'ok'
    return jsonify(answer)


@app.route("/update_user_group", methods=["POST"])
def update_user_group():
    answer = {'id': 0, 'answer': 'error'}
    if request.method == 'POST':
        post_data = request.get_json()
        user_id = post_data['id']
        group_id = post_data['group_id']
        if group_id is None:
            answer['answer'] = 'ERROR'
        else:
            main_user_id = db.session.query(User).get(user_id)
            main_group_id = db.session.query(Group).get(group_id)
            main_user_id._groups.append(main_group_id)
            db.session.commit()
            answer['answer'] = 'ok'

    return jsonify(answer)


@app.route("/delete_user_group", methods=["POST"])
def delete_user_group():
    answer = {'id': 0, 'answer': 'error'}
    if request.method == 'POST':
        post_data = request.get_json()
        user_id = post_data['id']
        group_id = post_data['group_id']
        main_user_id = db.session.query(User).get(user_id)
        main_group_id = db.session.query(Group).get(group_id)
        main_user_id._groups.remove(main_group_id)
        db.session.commit()

        answer['answer'] = 'ok'
    return jsonify(answer)


@app.route('/roles', methods=["GET", "POST"])
def roles():
    data_roles = db.session.query(Role).all()

    return jsonify({
        'data_roles': [i.serialize for i in data_roles],
    })


@app.route("/add_role", methods=["GET", "POST"])
def role_add():
    answer = {'answer': 'error'}
    if request.method == 'POST':
        post_data = request.get_json()
        if post_data['role_name'] is not None:
            role = Role(name=post_data['role_name'])
            db.session.add(role)
            db.session.commit()
            answer['answer'] = 'ok'
        else:
            answer['answer'] = 'ERROR'
    return jsonify(answer)


@app.route("/delete_role", methods=["POST"])
def delete_role():
    answer = {'id': 0, 'answer': 'error'}
    if request.method == 'POST':
        post_data = request.get_json()
        role_id = post_data['role_id']
        role = Role.query.filter_by(id=role_id).first()
        role.groups.clear()
        role.users.clear()
        db.session.commit()
        db.session.delete(role)
        db.session.commit()
        answer['answer'] = 'ok'
    return jsonify(answer)


@app.route("/update_role_name", methods=["POST"])
def update_role_name():
    answer = {'id': 0, 'answer': 'error'}
    if request.method == 'POST':
        post_data = request.get_json()
        role_id = post_data['role_id']
        new_role_name = post_data['role_name']
        if new_role_name == "administrator" or new_role_name == "employee":
            answer['answer'] = 'ERROR'
        else:
            role = db.session.query(Role).filter_by(id=role_id).first()
            role.name = new_role_name
            db.session.commit()

        answer['answer'] = 'ok'

    return jsonify(answer)


@app.route("/update_role_user", methods=["POST"])
def update_role_user():
    answer = {'id': 0, 'answer': 'error'}
    if request.method == 'POST':
        post_data = request.get_json()
        role_id = post_data['role_id']
        user_id = post_data['user_id']
        main_user_id = db.session.query(User).get(user_id)
        main_role_id = db.session.query(Role).get(role_id)
        if main_role_id.name == "employee":
            admin_object = Role.query.filter_by(name="administrator").first()
            for obj in main_user_id._roles:
                if obj == admin_object:
                    main_user_id._roles.remove(obj)
                    db.session.commit()
                    main_user_id._roles.append(main_role_id)
                    db.session.commit();
                    # main_role_id.users.append(main_user_id)
                    # db.session.commit()
        elif main_role_id.name == "administrator":
            employee_object = Role.query.filter_by(name="employee").first()
            for obj in main_user_id._roles:
                if obj == employee_object:
                    main_user_id._roles.remove(obj)
                    db.session.commit()
                    main_user_id._roles.append(main_role_id)
                    db.session.commit()
        else:
            main_user_id._roles.append(main_role_id)
            db.session.commit()
        answer['answer'] = 'ok'

    return jsonify(answer)


@app.route('/groups', methods=["GET", "POST"])
def groups():
    data_groups = db.session.query(Group).all()
    return jsonify({
        'data_groups': [i.serialize for i in data_groups],
    })


@app.route("/delete_role_user", methods=["POST"])
def delete_role_user():
    answer = {'id': 0, 'answer': 'error'}
    if request.method == 'POST':
        post_data = request.get_json()
        role_id = post_data['role_id']
        user_id = post_data['user_id']
        main_user_id = db.session.query(User).get(user_id)
        main_role_id = db.session.query(Role).get(role_id)
        main_role_id.users.remove(main_user_id)
        db.session.commit()
        answer['answer'] = 'ok'
    return jsonify(answer)


@app.route('/get_user', methods=['GET', 'POST'])
def get_user():
    answer = {'id': 0, 'answer': 'error'}
    # print(user)
    if request.method == 'POST':
        post_data = request.get_json()
        user_id = post_data['id']
        print(user_id)
        user = db.session.query(User).filter_by(id=user_id).first()
        all_roles = db.session.query(Role).all()
        all_groups = db.session.query(Group).all()
        answer['user'] = user.serialize
        answer['all_roles'] = [i.serialize for i in all_roles]
        answer['all_groups'] = [i.serialize for i in all_groups]
        answer['answer'] = 'ok'

    return jsonify(answer)


@app.route("/update_role_group", methods=["POST"])
def update_role_group():
    answer = {'id': 0, 'answer': 'error'}
    if request.method == 'POST':
        post_data = request.get_json()
        role_id = post_data['role_id']
        group_id = post_data['group_id']
        if role_id is None:
            answer['answer'] = 'ERROR'
        else:
            main_group_id = db.session.query(Group).get(group_id)
            main_role_id = db.session.query(Role).get(role_id)
            main_role_id.groups.append(main_group_id)
            db.session.commit()
        answer['answer'] = 'ok'

    return jsonify(answer)


@app.route("/delete_group_role", methods=["POST"])
def delete_group_role():
    answer = {'id': 0, 'answer': 'error'}
    if request.method == 'POST':
        post_data = request.get_json()
        role_id = post_data['role_id']
        group_id = post_data['group_id']
        main_role_id = db.session.query(Role).get(role_id)
        main_group_id = db.session.query(Group).get(group_id)
        main_role_id.groups.remove(main_group_id)
        db.session.commit()
        answer['answer'] = 'ok'
    return jsonify(answer)


@app.route("/add_group", methods=["GET", "POST"])
def group_add():
    answer = {'id': 0, 'answer': 'error'}
    if request.method == 'POST':
        post_data = request.get_json()
        group_name = post_data['group_name']
        group = Group(name=group_name)
        db.session.add(group)
        db.session.commit()
        answer['answer'] = 'ok'
    return jsonify(answer)


@app.route("/delete_group", methods=["POST"])
def delete_group():
    answer = {'id': 0, 'answer': 'error'}
    if request.method == 'POST':
        post_data = request.get_json()
        group_id = post_data['group_id']
        group = Group.query.filter_by(id=group_id).first()
        group.users.clear()
        group._roles.clear()
        db.session.commit()
        db.session.delete(group)
        db.session.commit()
        answer['answer'] = 'ok'
    return jsonify(answer)


@app.route("/update_group_name", methods=["POST"])
def update_group_name():
    answer = {'id': 0, 'answer': 'error'}
    if request.method == 'POST':
        post_data = request.get_json()
        group_id = post_data['group_id']
        new_group_name = post_data['group_name']
        group = db.session.query(Group).filter_by(id=group_id).first()
        group.name = new_group_name
        db.session.commit()

        answer['answer'] = 'ok'

    return jsonify(answer)


@app.route("/update_group_user", methods=["POST"])
def update_group_user():
    answer = {'id': 0, 'answer': 'error'}
    if request.method == 'POST':
        post_data = request.get_json()
        user_id = post_data['group_id']
        group_id = post_data['user_id']
        if group_id is None:
            answer['answer'] = 'Error'
        else:
            main_group_id = db.session.query(Group).get(user_id)
            main_user_id = db.session.query(User).get(group_id)
            main_user_id._groups.append(main_group_id)
            db.session.commit()
            answer['answer'] = 'ok'
    return jsonify(answer)


@app.route("/delete_group_user", methods=["POST"])
def delete_group_user():
    answer = {'id': 0, 'answer': 'error'}
    if request.method == 'POST':
        post_data = request.get_json()
        user_id = post_data['user_id']
        group_id = post_data['group_id']
        main_user_id = db.session.query(User).get(user_id)
        main_group_id = db.session.query(Group).get(group_id)
        main_group_id.users.remove(main_user_id)
        db.session.commit()

        answer['answer'] = 'ok'
    return jsonify(answer)


@app.route('/get_role', methods=['GET', 'POST'])
def get_role():
    answer = {'id': 0, 'answer': 'error'}
    if request.method == 'POST':
        post_data = request.get_json()
        role_id = post_data['id']
        print(role_id)
        role = db.session.query(Role).filter_by(id=role_id).first()
        all_users = db.session.query(User).all()
        all_groups = db.session.query(Group).all()
        answer['role'] = role.serialize
        answer['all_users'] = [i.serialize for i in all_users]
        answer['all_groups'] = [i.serialize for i in all_groups]
        answer['answer'] = 'ok'

    return jsonify(answer)


@app.route('/get_group', methods=['GET', 'POST'])
def get_group():
    answer = {'id': 0, 'answer': 'error'}
    if request.method == 'POST':
        post_data = request.get_json()
        group_id = post_data['id']
        print(group_id)
        group = db.session.query(Group).filter_by(id=group_id).first()
        all_users = db.session.query(User).all()
        all_groups = db.session.query(Group).all()
        answer['group'] = group.serialize
        answer['all_users'] = [i.serialize for i in all_users]
        answer['all_groups'] = [i.serialize for i in all_groups]
        answer['answer'] = 'ok'

    return jsonify(answer)


if __name__ == '__main__':
    app.run()
