import reflex as rx
from app.states.state import State


def nav_item(label: str, href: str, icon: str) -> rx.Component:
    is_active = State.current_page == href.strip("/")
    return rx.el.a(
        rx.icon(icon, class_name="h-5 w-5 shrink-0"),
        rx.el.span(label, class_name="text-sm font-medium"),
        href=href,
        class_name=rx.cond(
            is_active,
            "flex items-center gap-3 rounded-lg bg-orange-100 px-3 py-2 text-orange-600 transition-all hover:text-orange-600",
            "flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900",
        ),
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.a(
                rx.icon("calendar-days", class_name="h-6 w-6 text-orange-600"),
                rx.el.span("Scheduler", class_name="sr-only"),
                href="/",
                class_name="flex items-center gap-2 text-lg font-semibold",
            ),
            class_name="flex h-16 items-center border-b px-6 shrink-0",
        ),
        rx.el.nav(
            nav_item("Dashboard", "/", "layout-dashboard"),
            nav_item("Teachers", "/teachers", "users"),
            nav_item("Classes", "/classes", "book-open"),
            nav_item("Schedules", "/schedules", "calendar-check"),
            nav_item("Rules", "/rules", "gavel"),
            nav_item("Subject Requirements", "/subject_requirements", "book-check"),
            class_name="flex-1 overflow-auto py-2 grid items-start px-4 text-sm font-medium",
        ),
        class_name="hidden border-r bg-gray-50/40 md:block w-64",
    )