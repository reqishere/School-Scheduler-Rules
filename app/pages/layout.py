import reflex as rx
from app.components.sidebar import sidebar
from app.components.header import header
from app.components.modals import app_modal


def main_layout(child: rx.Component) -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            header(),
            rx.el.main(child, class_name="flex-1 p-4 sm:p-6 md:p-8"),
            class_name="flex flex-col flex-1",
        ),
        app_modal(),
        class_name="flex min-h-screen w-full bg-gray-50/70 font-['Roboto']",
    )