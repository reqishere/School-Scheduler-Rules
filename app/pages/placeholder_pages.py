import reflex as rx
from app.pages.layout import main_layout
from app.states.state import State
from app.pages.schedules import ScheduleState


def stat_card(label: str, value: rx.Var, icon: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-6 w-6 text-gray-500"),
            class_name="p-3 bg-gray-100 rounded-lg",
        ),
        rx.el.div(
            rx.el.p(label, class_name="text-sm font-medium text-gray-500"),
            rx.el.p(value, class_name="text-2xl font-semibold text-gray-900"),
        ),
        class_name="flex items-center gap-4 p-4 bg-white border border-gray-200 rounded-xl shadow-sm",
    )


def teacher_compliance_row(teacher: rx.Var[dict]) -> rx.Component:
    hours = State.teacher_hours.get(teacher["id"], 0)
    min_hours = State.teacher_rules.get(teacher["id"], 0)
    progress = rx.cond(min_hours > 0, hours / min_hours * 100, 100)
    progress_color = rx.cond(
        progress >= 100,
        "bg-green-500",
        rx.cond(progress > 50, "bg-yellow-500", "bg-red-500"),
    )
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.image(
                    src=f"https://api.dicebear.com/9.x/initials/svg?seed={teacher['name']}",
                    class_name="h-10 w-10 rounded-full border",
                ),
                rx.el.div(
                    rx.el.p(teacher["name"], class_name="font-medium text-gray-900"),
                    rx.el.p(teacher["email"], class_name="text-sm text-gray-500"),
                ),
                class_name="flex items-center gap-3",
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        class_name="h-2.5 rounded-full " + progress_color,
                        style={"width": progress.to_string() + "%"},
                    ),
                    class_name="w-full bg-gray-200 rounded-full h-2.5",
                ),
                rx.el.p(
                    f"{hours.to_string()}h / {min_hours}h",
                    class_name="text-sm text-gray-600 mt-1 text-right",
                ),
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.cond(
                hours >= min_hours,
                rx.el.span(
                    "Compliant",
                    class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800",
                ),
                rx.el.span(
                    "Non-Compliant",
                    class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800",
                ),
            ),
            class_name="px-6 py-4",
        ),
        class_name="border-b",
    )


def recent_schedule_item(schedule: rx.Var[dict]) -> rx.Component:
    teacher = ScheduleState.get_teacher_by_id.get(schedule["teacher_id"], {})
    cls = ScheduleState.get_class_by_id.get(schedule["class_id"], {})
    return rx.el.li(
        rx.el.div(
            rx.icon("calendar-check", class_name="h-5 w-5 text-orange-500"),
            class_name="p-2 bg-orange-100 rounded-full",
        ),
        rx.el.div(
            rx.el.p(cls.get("name", "..."), class_name="font-medium text-gray-800"),
            rx.el.p(
                f"{schedule['day_of_week']}, {schedule['start_time']}",
                class_name="text-sm text-gray-500",
            ),
            class_name="flex-1",
        ),
        rx.el.div(
            rx.image(
                src=f"https://api.dicebear.com/9.x/initials/svg?seed={teacher.get('name', '')}",
                class_name="h-8 w-8 rounded-full",
            ),
            rx.el.span(
                teacher.get("name", "..."),
                class_name="text-sm font-medium text-gray-700",
            ),
            class_name="flex items-center gap-2",
        ),
        class_name="flex items-center gap-4 p-3 hover:bg-gray-50 rounded-lg transition-colors",
    )


@rx.page(route="/")
def dashboard_page() -> rx.Component:
    return main_layout(
        rx.el.div(
            rx.el.h1(
                "Dashboard",
                class_name="text-2xl font-bold text-gray-800 tracking-tight mb-6",
            ),
            rx.el.div(
                stat_card("Total Teachers", State.teachers.length(), "users"),
                stat_card("Total Classes", State.classes.length(), "book-open"),
                stat_card("Total Schedules", State.schedules.length(), "calendar-days"),
                stat_card(
                    "Rule Compliance", State.rule_compliance.to_string() + "%", "gavel"
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Teacher Compliance",
                        class_name="text-xl font-semibold text-gray-800 mb-4",
                    ),
                    rx.el.div(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th(
                                        "Teacher",
                                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Weekly Hours",
                                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Status",
                                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                    ),
                                )
                            ),
                            rx.el.tbody(
                                rx.foreach(State.teachers, teacher_compliance_row),
                                class_name="bg-white divide-y divide-gray-200",
                            ),
                            class_name="min-w-full divide-y divide-gray-200",
                        ),
                        class_name="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg",
                    ),
                ),
                rx.el.div(
                    rx.el.h2(
                        "Recent Schedules",
                        class_name="text-xl font-semibold text-gray-800 mb-4",
                    ),
                    rx.el.div(
                        rx.el.ul(
                            rx.foreach(State.schedules.reverse(), recent_schedule_item),
                            class_name="space-y-2",
                        ),
                        class_name="bg-white border border-gray-200 rounded-xl p-4 shadow-sm h-full",
                    ),
                ),
                class_name="grid grid-cols-1 lg:grid-cols-3 gap-8",
            ),
            class_name="animate-fade-in",
        )
    )