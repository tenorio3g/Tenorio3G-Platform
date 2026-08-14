from flask import (
    redirect,
    render_template,
    request,
    session,
    url_for,
)


from . import identity

from app.domains.identity.people.bootstrap import (
    create_person,
    get_person,
    list_people,
    update_person,
)

from app.domains.identity.people.use_cases import (
    CreatePersonCommand,
    GetPersonQuery,
    UpdatePersonCommand,
)

from app.domains.identity.people.presentation import (
    PeoplePresenter,
)

from app.domains.identity.roles.bootstrap import (
    create_role,
    get_role,
    list_roles,
    update_role,
)

from app.domains.identity.roles.presentation import (
    RolesPresenter,
)

from app.domains.identity.roles.use_cases import (
    CreateRoleCommand,
    GetRoleQuery,
    UpdateRoleCommand,
)

from app.domains.identity.users.bootstrap import (
    create_user,
    list_users,
    password_hasher,
)

from app.domains.identity.users.presentation import (
    UsersPresenter,
)

from app.domains.identity.users.use_cases import (
    CreateUserCommand,
)

from app.domains.identity.people.bootstrap import (
    list_people,
)

from app.domains.identity.roles.bootstrap import (
    list_roles,
)


from app.domains.identity.users.bootstrap import (
    create_user,
    get_user,
    list_users,
    password_hasher,
    update_user,
)

from app.domains.identity.users.use_cases import (
    CreateUserCommand,
    GetUserQuery,
    UpdateUserCommand,
)

from app.domains.identity.authentication.bootstrap import (
    authenticate_user,
)

from app.domains.identity.authentication.use_cases import (
    AuthenticateUserCommand,
)

from app.domains.identity.authentication import (
    login_required,
    permission_required,
)

@identity.route("/personas")
@permission_required("people.view")
def people_index():

    result = list_people.execute()

    people = PeoplePresenter.present(
        result.people
    )

    return render_template(
        "pages/people/index.html",
        people=people,
    )

@identity.route(
    "/personas/nueva",
    methods=["GET", "POST"],
)
@permission_required("people.manage")
def create_person_route():

    if request.method == "POST":

        try:
            result = create_person.execute(
                CreatePersonCommand(
                    code=request.form.get(
                        "code",
                        "",
                    ),
                    name=request.form.get(
                        "name",
                        "",
                    ),
                    position=request.form.get(
                        "position",
                        "",
                    ),
                    is_active=True,
                )
            )

        except ValueError as exc:
            return (
                str(exc),
                400,
            )

        return redirect(
            url_for(
                "identity.people_index"
            )
        )

    return render_template(
        "pages/people/create.html"
    )

@identity.route(
    "/personas/<string:code>/editar",
    methods=["GET", "POST"],
)
@permission_required("people.manage")
def edit_person_route(code):

    result = get_person.execute(
        GetPersonQuery(
            code=code,
        )
    )

    person = result.person

    if person is None:
        return (
            "person not found",
            404,
        )

    if request.method == "POST":

        try:
            update_person.execute(
                UpdatePersonCommand(
                    code=code,
                    name=request.form.get(
                        "name",
                        "",
                    ),
                    position=request.form.get(
                        "position",
                        "",
                    ),
                    is_active=person.is_active,
                )
            )

        except ValueError as exc:
            return (
                str(exc),
                400,
            )

        return redirect(
            url_for(
                "identity.people_index"
            )
        )

    return render_template(
        "pages/people/edit.html",
        person=person,
    )

@identity.route(
    "/personas/<string:code>/estado",
    methods=["POST"],
)
@permission_required("people.manage")
def toggle_person_status_route(code):

    result = get_person.execute(
        GetPersonQuery(
            code=code,
        )
    )

    person = result.person

    if person is None:
        return (
            "person not found",
            404,
        )

    update_person.execute(
        UpdatePersonCommand(
            code=person.code,
            name=person.name,
            position=person.position,
            is_active=not person.is_active,
        )
    )

    return redirect(
        url_for(
            "identity.people_index"
        )
    )

@identity.route("/roles")
@permission_required("roles.view")
def roles_index():

    result = list_roles.execute()

    roles = RolesPresenter.present(
        result.roles
    )

    return render_template(
        "pages/roles/index.html",
        roles=roles,
    )


@identity.route(
    "/roles/nuevo",
    methods=["GET", "POST"],
)
@permission_required("roles.manage")

def create_role_route():

    if request.method == "POST":

        try:
            create_role.execute(
                CreateRoleCommand(
                    code=request.form.get(
                        "code",
                        "",
                    ),
                    name=request.form.get(
                        "name",
                        "",
                    ),
                    description=request.form.get(
                        "description",
                        "",
                    ),
                )
            )

        except ValueError as exc:
            return (
                str(exc),
                400,
            )

        return redirect(
            url_for(
                "identity.roles_index"
            )
        )

    return render_template(
        "pages/roles/create.html"
    )

@identity.route(
    "/roles/<string:code>/editar",
    methods=["GET", "POST"],
)
@permission_required("roles.manage")
def edit_role_route(code):

    result = get_role.execute(
        GetRoleQuery(
            code=code,
        )
    )

    role = result.role

    if role is None:
        return (
            "role not found",
            404,
        )

    if request.method == "POST":

        try:
            update_role.execute(
                UpdateRoleCommand(
                    code=role.code,
                    name=request.form.get(
                        "name",
                        "",
                    ),
                    description=request.form.get(
                        "description",
                        "",
                    ),
                    is_active=role.is_active,
                )
            )

        except ValueError as exc:
            return (
                str(exc),
                400,
            )

        return redirect(
            url_for(
                "identity.roles_index"
            )
        )

    return render_template(
        "pages/roles/edit.html",
        role=role,
    )


@identity.route(
    "/roles/<string:code>/estado",
    methods=["POST"],
)
@permission_required("roles.manage")
def toggle_role_status_route(code):

    result = get_role.execute(
        GetRoleQuery(
            code=code,
        )
    )

    role = result.role

    if role is None:
        return (
            "role not found",
            404,
        )

    update_role.execute(
        UpdateRoleCommand(
            code=role.code,
            name=role.name,
            description=role.description,
            is_active=not role.is_active,
        )
    )

    return redirect(
        url_for(
            "identity.roles_index"
        )
    )


@identity.route("/usuarios")
@permission_required("users.view")
def users_index():

    users_result = list_users.execute()
    people_result = list_people.execute()
    roles_result = list_roles.execute()

    users = UsersPresenter.present(
        users_result.users,
        people_result.people,
        roles_result.roles,
    )

    return render_template(
        "pages/users/index.html",
        users=users,
    )

@identity.route(
    "/usuarios/nuevo",
    methods=["GET", "POST"],
)
@permission_required("users.manage")
def create_user_route():

    people_result = list_people.execute()
    roles_result = list_roles.execute()

    if request.method == "POST":

        try:
            password_hash = (
                password_hasher.hash(
                    request.form.get(
                        "password",
                        "",
                    )
                )
            )

            create_user.execute(
                CreateUserCommand(
                    username=request.form.get(
                        "username",
                        "",
                    ),
                    password_hash=password_hash,
                    person_code=request.form.get(
                        "person_code",
                        "",
                    ),
                    role_code=request.form.get(
                        "role_code",
                        "",
                    ),
                )
            )

        except ValueError as exc:
            return (
                str(exc),
                400,
            )

        return redirect(
            url_for(
                "identity.users_index"
            )
        )

    return render_template(
        "pages/users/create.html",
        people=people_result.people,
        roles=roles_result.roles,
    )
@identity.route(
    "/usuarios/<string:username>/editar",
    methods=["GET", "POST"],
)
@permission_required("users.manage")
def edit_user_route(username):

    user_result = get_user.execute(
        GetUserQuery(
            username=username,
        )
    )

    user = user_result.user

    if user is None:
        return (
            "user not found",
            404,
        )

    people_result = list_people.execute()
    roles_result = list_roles.execute()

    if request.method == "POST":

        try:
            update_user.execute(
                UpdateUserCommand(
                    username=user.username,
                    password_hash=user.password_hash,
                    person_code=request.form.get(
                        "person_code",
                        "",
                    ),
                    role_code=request.form.get(
                        "role_code",
                        "",
                    ),
                    is_active=user.is_active,
                )
            )

        except ValueError as exc:
            return (
                str(exc),
                400,
            )

        return redirect(
            url_for(
                "identity.users_index"
            )
        )

    return render_template(
        "pages/users/edit.html",
        user=user,
        people=people_result.people,
        roles=roles_result.roles,
    )

@identity.route(
    "/usuarios/<string:username>/estado",
    methods=["POST"],
)
@permission_required("users.manage")
def toggle_user_status_route(username):

    user_result = get_user.execute(
        GetUserQuery(
            username=username,
        )
    )

    user = user_result.user

    if user is None:
        return (
            "user not found",
            404,
        )

    update_user.execute(
        UpdateUserCommand(
            username=user.username,
            password_hash=user.password_hash,
            person_code=user.person_code,
            role_code=user.role_code,
            is_active=not user.is_active,
        )
    )

    return redirect(
        url_for(
            "identity.users_index"
        )
    )


@identity.route(
    "/login",
    methods=["GET", "POST"],
)
def login_route():

    if request.method == "POST":

        result = authenticate_user.execute(
            AuthenticateUserCommand(
                username=request.form.get(
                    "username",
                    "",
                ),
                password=request.form.get(
                    "password",
                    "",
                ),
            )
        )

        if not result.authenticated:

            return render_template(
                "pages/login.html",
                error=(
                    "Usuario o contraseña incorrectos."
                ),
            ), 401

        user = result.user

        session.clear()

        session["username"] = (
            user.username
        )

        session["person_code"] = (
            user.person_code
        )

        session["role_code"] = (
            user.role_code
        )

        return redirect(
            url_for(
                "assets.index"
            )
        )

    return render_template(
        "pages/login.html"
    )

@identity.route(
    "/logout",
    methods=["POST"],
)
def logout_route():

    session.clear()

    return redirect(
        url_for(
            "identity.login_route"
        )
    )