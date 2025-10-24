import reflex as rx
from app.states.state import State
from app.pages.layout import main_layout
from app.pages.schedules import ScheduleState


def requirement_card(req: rx.Var[dict]) -> rx.Component:
    """Renders a card for a single subject requirement."""
    cls = ScheduleState.get_class_by_id.get(req["class_id"], {})
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("book-check", class_name="h-6 w-6 text-purple-500"),
                class_name="p-3 bg-purple-100 rounded-lg",
            ),
            rx.el.div(
                rx.el.h3(
                    cls.get("name", "Unknown Class"),
                    class_name="font-semibold text-gray-800",
                ),
                rx.el.p(
                    f"Requires subject: {req['subject']}",
                    class_name="text-sm text-gray-500",
                ),
            ),
            class_name="flex items-center gap-4",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("pencil", class_name="h-4 w-4"),
                on_click=lambda: State.open_modal("subject_requirement", req["id"]),
                class_name="p-2 rounded-md text-gray-500 hover:text-gray-800 hover:bg-gray-100 transition-colors",
            ),
            rx.el.button(
                rx.icon("trash-2", class_name="h-4 w-4"),
                on_click=lambda: State.delete_subject_requirement(req["id"]),
                class_name="p-2 rounded-md text-red-500 hover:text-red-700 hover:bg-red-50 transition-colors",
            ),
            class_name="flex items-center gap-1",
        ),
        class_name="flex items-center justify-between p-4 bg-white border border-gray-200 rounded-xl shadow-sm",
    )


@rx.page(route="/subject_requirements")
def subject_requirements_page() -> rx.Component:
    """The page for managing subject requirements for classes."""
    return main_layout(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Subject Requirements",
                        class_name="text-2xl font-bold text-gray-800 tracking-tight",
                    ),
                    rx.el.p(
                        "Manage required subjects for each class.",
                        class_name="text-gray-500",
                    ),
                ),
                rx.el.button(
                    rx.icon("plus", class_name="mr-2 h-4 w-4"),
                    "Add Requirement",
                    on_click=lambda: State.open_modal("subject_requirement"),
                    class_name="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 bg-orange-600 text-white shadow hover:bg-orange-600/90 h-9 px-4 py-2",
                ),
                class_name="flex items-center justify-between mb-6",
            ),
            rx.cond(
                State.subject_requirements.length() > 0,
                rx.el.div(
                    rx.foreach(State.subject_requirements, requirement_card),
                    class_name="grid gap-4 md:grid-cols-2 lg:grid-cols-3",
                ),
                rx.el.div(
                    rx.icon("book-check", class_name="h-12 w-12 text-gray-400 mb-4"),
                    rx.el.h3(
                        "No Subject Requirements Found",
                        class_name="text-lg font-semibold text-gray-700",
                    ),
                    rx.el.p(
                        "Add your first requirement to get started.",
                        class_name="text-sm text-gray-500",
                    ),
                    class_name="flex flex-col items-center justify-center text-center p-8 border-2 border-dashed border-gray-200 rounded-xl",
                ),
            ),
            class_name="animate-fade-in",
        )
    )