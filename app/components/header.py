import reflex as rx


def header() -> rx.Component:
    """Renders the top header bar of the application."""
    return rx.el.header(
        rx.el.div(
            rx.el.h1(
                "School Scheduler", class_name="text-lg font-semibold text-gray-700"
            )
        ),
        rx.el.div(
            rx.image(
                src=f"https://api.dicebear.com/9.x/initials/svg?seed=Admin",
                class_name="h-8 w-8 rounded-full border border-gray-200",
            ),
            class_name="flex items-center gap-4",
        ),
        class_name="flex items-center justify-between h-16 border-b bg-white px-6 sticky top-0 z-30",
    )