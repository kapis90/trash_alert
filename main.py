import os
from dotenv import load_dotenv
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
from fasthtml.oauth import GoogleAppClient, OAuth
from supabase import Client, create_client


class Auth(OAuth):
    def get_auth(self, info, ident, session, state):
        email = info.email or ""
        if info.email_verified and email.split("@")[-1] == "answer.ai":
            return RedirectResponse("/", status_code=303)


app, rt = fast_app(before=[lambda req, session: session.setdefault("auth", None)])
load_dotenv()
google_client = GoogleAppClient(
    os.getenv("AUTH_CLIENT_ID"), os.getenv("AUTH_CLIENT_SECRET")
)
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

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
        render_message_list(),
    )


def get_messages():
    # Sort by 'id' in descending order to get the latest entries first
    response = (
        supabase.table("streets_mapping").select("*").order("id", desc=False).execute()
    )
    return response.data


def render_message_list():
    messages = get_messages()
    return Div(
        *[render_message(entry) for entry in messages],
        id="message-list",
    )


def render_message(entry):
    return (
        Article(
            Header(f"Obszar: {entry['area']}"),
            P(entry["streets"]),
        ),
    )


@rt("/")
def get():
    return Titled(
        "Alert śmieciowy!",
        Div(
            A("Zaloguj się", href="/login"),
            style="text-align: right",
        ),
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
                    Small(A("Log In with Google", href=oauth.login_link(req))),
                    Button("Zaloguj", type="submit"),
                    style="width: 300px; margin: 0 auto; padding: 20px; border: 1px solid #ccc; border-radius: 5px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);",
                ),
            ),
        ),
        style="text-align: center;",
    )


# @app.get('/login')
# def login(req): return Div(P("Not logged in"), A('Log in', href=oauth.login_link(req)))

serve()
