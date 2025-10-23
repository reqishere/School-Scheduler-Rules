import reflex as rx
from app.states.state import State
from app.pages.layout import main_layout


def class_card(cls: rx.Var[dict]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("book-open", class_name="h-6 w-6 text-orange-500"),
                class_name="p-3 bg-orange-100 rounded-lg",
            ),
            rx.el.div(
                rx.el.h3(
                    cls["name"], class_name="text-base font-semibold text-gray-800"
                ),
                rx.el.div(
                    rx.el.span(
                        cls["subject"],
                        class_name="text-xs font-medium bg-gray-100 text-gray-600 px-2 py-1 rounded-full",
                    ),
                    rx.el.span(
                        f"{cls['duration']} mins",
                        class_name="text-xs font-medium bg-blue-100 text-blue-600 px-2 py-1 rounded-full",
                    ),
                    class_name="flex items-center gap-2 mt-1",
                ),
                class_name="flex-1",
            ),
            class_name="flex items-start gap-4",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("pencil", class_name="h-4 w-4"),
                on_click=lambda: State.open_modal("class", cls["id"]),
                class_name="p-2 rounded-md text-gray-500 hover:text-gray-800 hover:bg-gray-100 transition-colors",
            ),
            rx.el.button(
                rx.icon("trash-2", class_name="h-4 w-4"),
                on_click=lambda: State.delete_class(cls["id"]),
                class_name="p-2 rounded-md text-red-500 hover:text-red-700 hover:bg-red-50 transition-colors",
            ),
            class_name="flex items-center gap-1",
        ),
        class_name="flex items-start justify-between p-4 bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-shadow",
    )


@rx.page(route="/classes")
def classes_page() -> rx.Component:
    return main_layout(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Classes",
                        class_name="text-2xl font-bold text-gray-800 tracking-tight",
                    ),
                    rx.el.p(
                        f"Manage the classes available for scheduling.",
                        class_name="text-gray-500",
                    ),
                ),
                rx.el.button(
                    rx.icon("plus", class_name="mr-2 h-4 w-4"),
                    "Add Class",
                    on_click=lambda: State.open_modal("class"),
                    class_name="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 bg-orange-600 text-white shadow hover:bg-orange-600/90 h-9 px-4 py-2",
                ),
                class_name="flex items-center justify-between mb-6",
            ),
            rx.cond(
                State.classes.length() > 0,
                rx.el.div(
                    rx.foreach(State.classes, class_card),
                    class_name="grid gap-4 md:grid-cols-2 lg:grid-cols-3",
                ),
                rx.el.div(
                    rx.icon("book-open", class_name="h-12 w-12 text-gray-400 mb-4"),
                    rx.el.h3(
                        "No Classes Found",
                        class_name="text-lg font-semibold text-gray-700",
                    ),
                    rx.el.p(
                        "Add your first class to get started.",
                        class_name="text-sm text-gray-500",
                    ),
                    class_name="flex flex-col items-center justify-center text-center p-8 border-2 border-dashed border-gray-200 rounded-xl",
                ),
            ),
            class_name="animate-fade-in",
        )
    )