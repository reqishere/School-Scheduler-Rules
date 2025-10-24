import reflex as rx
from app.states.state import State
from app.pages.layout import main_layout


def teacher_card(teacher: rx.Var[dict]) -> rx.Component:
    hours = State.teacher_hours.get(teacher["id"], 0)
    min_hours = State.teacher_rules.get(teacher["id"], 0)
    progress = rx.cond(min_hours > 0, hours / min_hours * 100, 0)
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.image(
                    src=f"https://api.dicebear.com/9.x/initials/svg?seed={teacher['name']}",
                    class_name="h-12 w-12 rounded-full border-2 border-white shadow-sm",
                ),
                rx.el.div(
                    rx.el.h3(
                        teacher["name"],
                        class_name="text-base font-semibold text-gray-800",
                    ),
                    rx.el.p(teacher["email"], class_name="text-sm text-gray-500"),
                    rx.el.span(
                        teacher["subject"],
                        class_name="text-xs font-medium bg-purple-100 text-purple-600 px-2 py-1 rounded-full",
                    ),
                ),
                class_name="flex items-center gap-4",
            )
        ),
        rx.el.div(
            rx.el.div(
                rx.el.button(
                    rx.icon("pencil", class_name="h-4 w-4"),
                    on_click=lambda: State.open_modal("teacher", teacher["id"]),
                    class_name="p-2 rounded-md text-gray-500 hover:text-gray-800 hover:bg-gray-100 transition-colors",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=lambda: State.delete_teacher(teacher["id"]),
                    class_name="p-2 rounded-md text-red-500 hover:text-red-700 hover:bg-red-50 transition-colors",
                ),
                class_name="flex items-center gap-1",
            ),
            class_name="flex items-center justify-between",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    f"{hours.to_string()}h / {min_hours}h",
                    class_name="text-sm font-medium text-gray-600",
                ),
                rx.cond(
                    (min_hours > 0) & (hours < min_hours),
                    rx.el.div(
                        rx.icon(
                            "flag_triangle_right", class_name="h-4 w-4 text-yellow-500"
                        ),
                        rx.el.span(
                            "Under hours",
                            class_name="text-xs font-semibold text-yellow-600",
                        ),
                        class_name="flex items-center gap-1 bg-yellow-100 px-2 py-1 rounded-full",
                    ),
                    rx.el.div(
                        rx.icon("check_check", class_name="h-4 w-4 text-green-500"),
                        rx.el.span(
                            "Met hours",
                            class_name="text-xs font-semibold text-green-600",
                        ),
                        class_name="flex items-center gap-1 bg-green-100 px-2 py-1 rounded-full",
                    ),
                ),
                class_name="flex justify-between items-center mb-2",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        class_name="bg-green-500 h-2 rounded-full",
                        style={"width": progress.to_string() + "%"},
                    ),
                    class_name="w-full bg-gray-200 rounded-full h-2",
                )
            ),
        ),
        class_name="flex flex-col gap-4 p-4 bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-shadow",
    )


@rx.page(route="/teachers")
def teachers_page() -> rx.Component:
    return main_layout(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Teachers",
                        class_name="text-2xl font-bold text-gray-800 tracking-tight",
                    ),
                    rx.el.p(
                        f"Manage your school's teachers.", class_name="text-gray-500"
                    ),
                ),
                rx.el.button(
                    rx.icon("plus", class_name="mr-2 h-4 w-4"),
                    "Add Teacher",
                    on_click=lambda: State.open_modal("teacher"),
                    class_name="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 bg-orange-600 text-white shadow hover:bg-orange-600/90 h-9 px-4 py-2",
                ),
                class_name="flex items-center justify-between mb-6",
            ),
            rx.cond(
                State.teachers.length() > 0,
                rx.el.div(
                    rx.foreach(State.teachers, teacher_card),
                    class_name="grid gap-4 md:grid-cols-2 lg:grid-cols-3",
                ),
                rx.el.div(
                    rx.icon("users", class_name="h-12 w-12 text-gray-400 mb-4"),
                    rx.el.h3(
                        "No Teachers Found",
                        class_name="text-lg font-semibold text-gray-700",
                    ),
                    rx.el.p(
                        "Add your first teacher to get started.",
                        class_name="text-sm text-gray-500",
                    ),
                    class_name="flex flex-col items-center justify-center text-center p-8 border-2 border-dashed border-gray-200 rounded-xl",
                ),
            ),
            class_name="animate-fade-in",
        )
    )