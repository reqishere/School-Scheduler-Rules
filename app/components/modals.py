import reflex as rx
from app.states.state import State


def _form_input(
    label: str,
    name: str,
    placeholder: str,
    value: rx.Var,
    on_change: rx.event.EventHandler,
    type: str = "text",
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="text-sm font-medium text-gray-700"),
        rx.el.input(
            name=name,
            placeholder=placeholder,
            default_value=value,
            on_change=on_change,
            type=type,
            class_name="mt-1 block w-full rounded-lg border-gray-200 bg-white px-4 py-2 text-gray-700 shadow-sm focus:border-orange-500 focus:ring-orange-500",
        ),
        class_name="mb-4",
    )


def teacher_modal_content() -> rx.Component:
    return rx.el.form(
        rx.el.h2(
            rx.cond(State.is_editing, "Edit Teacher", "Add New Teacher"),
            class_name="text-lg font-semibold text-gray-900 mb-4",
        ),
        _form_input(
            "Full Name",
            "teacher_name",
            "e.g. John Doe",
            State.teacher_name,
            State.set_teacher_name,
        ),
        _form_input(
            "Email Address",
            "teacher_email",
            "e.g. john.doe@school.com",
            State.teacher_email,
            State.set_teacher_email,
            type="email",
        ),
        rx.el.div(
            rx.el.button(
                "Cancel",
                on_click=State.close_modal,
                type="button",
                class_name="w-full justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2",
            ),
            rx.el.button(
                "Save Teacher",
                type="submit",
                class_name="w-full justify-center rounded-md border border-transparent bg-orange-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2",
            ),
            class_name="mt-5 sm:mt-6 grid grid-cols-2 gap-3",
        ),
        on_submit=State.save_teacher,
    )


def class_modal_content() -> rx.Component:
    return rx.el.form(
        rx.el.h2(
            rx.cond(State.is_editing, "Edit Class", "Add New Class"),
            class_name="text-lg font-semibold text-gray-900 mb-4",
        ),
        _form_input(
            "Class Name",
            "class_name",
            "e.g. Introduction to Physics",
            State.class_name,
            State.set_class_name,
        ),
        _form_input(
            "Subject",
            "class_subject",
            "e.g. Science",
            State.class_subject,
            State.set_class_subject,
        ),
        _form_input(
            "Duration (minutes)",
            "class_duration",
            "e.g. 60",
            State.class_duration,
            State.set_class_duration,
            type="number",
        ),
        rx.el.div(
            rx.el.button(
                "Cancel",
                on_click=State.close_modal,
                type="button",
                class_name="w-full justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2",
            ),
            rx.el.button(
                "Save Class",
                type="submit",
                class_name="w-full justify-center rounded-md border border-transparent bg-orange-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2",
            ),
            class_name="mt-5 sm:mt-6 grid grid-cols-2 gap-3",
        ),
        on_submit=State.save_class,
    )


def schedule_modal_content() -> rx.Component:
    return rx.el.form(
        rx.el.h2(
            rx.cond(State.is_editing, "Edit Schedule", "Add New Schedule"),
            class_name="text-lg font-semibold text-gray-900 mb-4",
        ),
        rx.el.div(
            rx.el.label("Class", class_name="text-sm font-medium text-gray-700"),
            rx.el.select(
                rx.el.option("Select a class", value="", disabled=True),
                rx.foreach(
                    State.classes,
                    lambda cls: rx.el.option(cls["name"], value=cls["id"].to_string()),
                ),
                value=State.schedule_class_id,
                on_change=State.set_schedule_class_id,
                class_name="mt-1 block w-full rounded-lg border-gray-200 bg-white px-4 py-2 text-gray-700 shadow-sm focus:border-orange-500 focus:ring-orange-500",
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.label("Teacher", class_name="text-sm font-medium text-gray-700"),
            rx.el.select(
                rx.el.option("Select a teacher", value="", disabled=True),
                rx.foreach(
                    State.teachers,
                    lambda teacher: rx.el.option(
                        teacher["name"], value=teacher["id"].to_string()
                    ),
                ),
                value=State.schedule_teacher_id,
                on_change=State.set_schedule_teacher_id,
                class_name="mt-1 block w-full rounded-lg border-gray-200 bg-white px-4 py-2 text-gray-700 shadow-sm focus:border-orange-500 focus:ring-orange-500",
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.label("Day of Week", class_name="text-sm font-medium text-gray-700"),
            rx.el.select(
                rx.foreach(
                    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                    lambda day: rx.el.option(day, value=day),
                ),
                value=State.schedule_day_of_week,
                on_change=State.set_schedule_day_of_week,
                class_name="mt-1 block w-full rounded-lg border-gray-200 bg-white px-4 py-2 text-gray-700 shadow-sm focus:border-orange-500 focus:ring-orange-500",
            ),
            class_name="mb-4",
        ),
        _form_input(
            "Start Time",
            "schedule_start_time",
            "e.g. 09:00",
            State.schedule_start_time,
            State.set_schedule_start_time,
            type="time",
        ),
        rx.el.div(
            rx.el.button(
                "Cancel",
                on_click=State.close_modal,
                type="button",
                class_name="w-full justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2",
            ),
            rx.el.button(
                "Save Schedule",
                type="submit",
                class_name="w-full justify-center rounded-md border border-transparent bg-orange-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2",
            ),
            class_name="mt-5 sm:mt-6 grid grid-cols-2 gap-3",
        ),
        on_submit=State.save_schedule,
    )


def app_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="bg-black/40 fixed inset-0 z-50"
            ),
            rx.radix.primitives.dialog.content(
                rx.match(
                    State.modal_type,
                    ("teacher", teacher_modal_content()),
                    ("class", class_modal_content()),
                    ("schedule", schedule_modal_content()),
                    ("rule", rule_modal_content()),
                    rx.el.div(),
                ),
                class_name="bg-white p-6 rounded-xl shadow-lg w-full max-w-md m-4 fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50",
            ),
        ),
        open=State.show_modal,
        on_open_change=lambda open_state: State.close_modal(),
    )


def rule_modal_content() -> rx.Component:
    return rx.el.form(
        rx.el.h2(
            rx.cond(State.is_editing, "Edit Rule", "Add New Rule"),
            class_name="text-lg font-semibold text-gray-900 mb-4",
        ),
        rx.el.div(
            rx.el.label("Teacher", class_name="text-sm font-medium text-gray-700"),
            rx.el.select(
                rx.el.option("Select a teacher", value="", disabled=True),
                rx.foreach(
                    State.teachers,
                    lambda teacher: rx.el.option(
                        teacher["name"], value=teacher["id"].to_string()
                    ),
                ),
                value=State.rule_teacher_id,
                on_change=State.set_rule_teacher_id,
                class_name="mt-1 block w-full rounded-lg border-gray-200 bg-white px-4 py-2 text-gray-700 shadow-sm focus:border-orange-500 focus:ring-orange-500",
            ),
            class_name="mb-4",
        ),
        _form_input(
            "Minimum Weekly Hours",
            "rule_min_hours",
            "e.g. 10",
            State.rule_min_hours,
            State.set_rule_min_hours,
            type="number",
        ),
        rx.el.div(
            rx.el.button(
                "Cancel",
                on_click=State.close_modal,
                type="button",
                class_name="w-full justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2",
            ),
            rx.el.button(
                "Save Rule",
                type="submit",
                class_name="w-full justify-center rounded-md border border-transparent bg-orange-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2",
            ),
            class_name="mt-5 sm:mt-6 grid grid-cols-2 gap-3",
        ),
        on_submit=State.save_rule,
    )