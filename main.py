import os
from pathlib import Path
from dotenv import load_dotenv
from fasthtml.svg import Svg, NotStr
from fasthtml.common import (
    Form,
    Fieldset,
    Input,
    Button,
    Titled,
    Div,
    P,
    Em,
    Hr,
    fast_app,
    serve,
    Article,
    Footer,
    Header,
    Small,
    A,
    RedirectResponse,
)
from fasthtml.oauth import GoogleAppClient, OAuth, http_patterns
from src.backend.database.db_queries import DatabaseQueries
from src.backend.database.model import Area


class Auth(OAuth):
    def __init__(
        self,
        app,
        cli,
        skip=None,
        redir_path="/redirect",
        error_path="/error",
        logout_path="/logout",
        login_path="/",
        https=True,
        http_patterns=http_patterns,
    ):
        super().__init__(
            app,
            cli,
            skip,
            redir_path,
            error_path,
            logout_path,
            login_path,
            https,
            http_patterns,
        )
        self.active_user = None

    def get_auth(self, info, ident, session, state):
        if not info.email_verified:
            return RedirectResponse("/", status_code=303)
        if user := db_queries.get_user_by_email(info.email):
            self.active_user = user
            return
        self.active_user = db_queries.insert_user(username=info.name, email=info.email)


app, rt = fast_app()
load_dotenv()
google_client = GoogleAppClient(
    os.getenv("AUTH_CLIENT_ID"), os.getenv("AUTH_CLIENT_SECRET")
)
db_queries = DatabaseQueries()

oauth = Auth(app, google_client, skip=["/redirect", "/error", "/login", "/"])


def render_content():
    # form = Form(
    #     Fieldset(
    #         Input(
    #             type="text",
    #             name="name",
    #             placeholder="Name",
    #             required=True,
    #             maxlength=15,
    #         ),
    #         Input(
    #             type="text",
    #             name="message",
    #             placeholder="Message",
    #             required=True,
    #             maxlength=15,
    #         ),
    #         Button("Submit", type="submit"),
    #         role="group",
    #     ),
    # )

    return Div(
        P(Em("Obszary objęte alertem:")),
        Hr(),
        render_area_list(),
    )


def render_area_list():
    areas = db_queries.get_areas()
    return Div(
        *[render_area_summary(area) for area in areas],
        id="area-list",
    )


def render_area_summary(area: Area):
    streets = ", ".join(
        [f"ul. {street.name}" for street in db_queries.get_streets_by_area_id(area.id)]
    )
    return (
        Article(
            Header(f"Obszar: {area.name}"),
            P(streets),
        ),
    )


def render_login_content():
    if oauth.active_user:
        return Div(
            P(f"Witaj {oauth.active_user.name}!"),
            A("Wyloguj się", href="/logout"),
            style="text-align: right",
        )
    else:
        return Div(
            A("Zaloguj się", href="/login"),
            style="text-align: right",
        )


@rt("/")
def get():
    return Titled(
        "Alert śmieciowy!",
        render_login_content(),
        render_content(),
    )


@app.get("/login")
def login(req):
    return Titled(
        "Logowanie",
        Div(A("Powrót", href="/"), style="text-align: right"),
        Div(
            Form(
                Fieldset(
                    Input(
                        type="text",
                        name="login",
                        placeholder="Login",
                        required=True,
                    ),
                    Input(
                        type="password",
                        name="password",
                        placeholder="Hasło",
                        required=True,
                    ),
                    Small(A("Zarejestruj się!", href="/register")),
                    Button("Zaloguj", type="submit"),
                    A(
                        NotStr(Path("./assets/web_dark_rd_SI.svg").read_text()),
                        href=oauth.login_link(req),
                    ),
                    style="width: 300px; margin: 0 auto; padding: 20px; border: 1px solid #ccc; border-radius: 5px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);",
                ),
            ),
        ),
        style="text-align: center;",
    )


serve()
