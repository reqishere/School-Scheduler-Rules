import reflex as rx
from app.states.state import State
from app.pages import (
    dashboard_page,
    teachers_page,
    classes_page,
    schedules_page,
    rules_page,
    subject_requirements_page,
)

app = rx.App(
    theme=rx.theme(appearance="light", accent_color="orange"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap",
            rel="stylesheet",
        ),
    ],
)