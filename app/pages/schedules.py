import reflex as rx
from app.states.state import State, Teacher, Class
from app.pages.layout import main_layout


class ScheduleState(rx.State):
    @rx.var
    async def get_teacher_by_id(self) -> dict[int, dict]:
        state = await self.get_state(State)
        return {teacher["id"]: teacher for teacher in state.teachers}

    @rx.var
    async def get_class_by_id(self) -> dict[int, dict]:
        state = await self.get_state(State)
        return {cls["id"]: cls for cls in state.classes}


def schedule_card(schedule: rx.Var[dict]) -> rx.Component:
    teacher = ScheduleState.get_teacher_by_id.get(schedule["teacher_id"], {})
    cls = ScheduleState.get_class_by_id.get(schedule["class_id"], {})
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    cls.get("name", "Unknown Class"),
                    class_name="font-semibold text-gray-800",
                ),
                rx.el.p(
                    f"{schedule['day_of_week']}, {schedule['start_time']} - {schedule['end_time']}",
                    class_name="text-sm text-gray-500",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.image(
                    src=f"https://api.dicebear.com/9.x/initials/svg?seed={teacher.get('name', 'N/A')}",
                    class_name="h-8 w-8 rounded-full border border-gray-200",
                ),
                rx.el.span(
                    teacher.get("name", "Unknown Teacher"),
                    class_name="text-sm font-medium",
                ),
                class_name="flex items-center gap-2",
            ),
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("pencil", class_name="h-4 w-4"),
                on_click=lambda: State.open_modal("schedule", schedule["id"]),
                class_name="p-2 rounded-md text-gray-500 hover:text-gray-800 hover:bg-gray-100 transition-colors",
            ),
            rx.el.button(
                rx.icon("trash-2", class_name="h-4 w-4"),
                on_click=lambda: State.delete_schedule(schedule["id"]),
                class_name="p-2 rounded-md text-red-500 hover:text-red-700 hover:bg-red-50 transition-colors",
            ),
            class_name="flex items-center gap-1",
        ),
        class_name="flex items-center justify-between p-4 bg-white border border-gray-200 rounded-xl shadow-sm",
    )


@rx.page(route="/schedules")
def schedules_page() -> rx.Component:
    return main_layout(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Schedules",
                        class_name="text-2xl font-bold text-gray-800 tracking-tight",
                    ),
                    rx.el.p(
                        "Manage class schedules and teacher assignments.",
                        class_name="text-gray-500",
                    ),
                ),
                rx.el.button(
                    rx.icon("plus", class_name="mr-2 h-4 w-4"),
                    "Add Schedule",
                    on_click=lambda: State.open_modal("schedule"),
                    class_name="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 bg-orange-600 text-white shadow hover:bg-orange-600/90 h-9 px-4 py-2",
                ),
                class_name="flex items-center justify-between mb-6",
            ),
            rx.cond(
                State.schedules.length() > 0,
                rx.el.div(
                    rx.foreach(State.schedules, schedule_card), class_name="grid gap-4"
                ),
                rx.el.div(
                    rx.icon(
                        "calendar-check", class_name="h-12 w-12 text-gray-400 mb-4"
                    ),
                    rx.el.h3(
                        "No Schedules Found",
                        class_name="text-lg font-semibold text-gray-700",
                    ),
                    rx.el.p(
                        "Create your first schedule to get started.",
                        class_name="text-sm text-gray-500",
                    ),
                    class_name="flex flex-col items-center justify-center text-center p-8 border-2 border-dashed border-gray-200 rounded-xl",
                ),
            ),
            class_name="animate-fade-in",
        )
    )