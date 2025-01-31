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
)
from supabase import Client, create_client

app, rt = fast_app()

load_dotenv()

supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


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
    response = supabase.table("streets_mapping").select("*").order("id", desc=False).execute()
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
    return Titled("Alert śmieciowy!", render_content())


serve()
