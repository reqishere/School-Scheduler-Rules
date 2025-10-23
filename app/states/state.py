import reflex as rx
from typing import TypedDict, Literal


class Teacher(TypedDict):
    id: int
    name: str
    email: str


class Class(TypedDict):
    id: int
    name: str
    subject: str
    duration: int


class Schedule(TypedDict):
    id: int
    class_id: int
    teacher_id: int
    day_of_week: Literal["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    start_time: str
    end_time: str


class Rule(TypedDict):
    id: int
    teacher_id: int
    min_hours: int


ModalType = Literal["teacher", "class", "schedule", "rule", ""]


class State(rx.State):
    teachers: list[Teacher] = [
        {"id": 1, "name": "John Doe", "email": "john.doe@example.com"},
        {"id": 2, "name": "Jane Smith", "email": "jane.smith@example.com"},
        {"id": 3, "name": "Peter Jones", "email": "peter.jones@example.com"},
    ]
    classes: list[Class] = [
        {"id": 1, "name": "Algebra 101", "subject": "Math", "duration": 60},
        {"id": 2, "name": "World History", "subject": "History", "duration": 90},
        {"id": 3, "name": "Physics I", "subject": "Science", "duration": 120},
    ]
    schedules: list[Schedule] = []
    rules: list[Rule] = [
        {"id": 1, "teacher_id": 1, "min_hours": 10},
        {"id": 2, "teacher_id": 2, "min_hours": 8},
    ]
    show_modal: bool = False
    modal_type: ModalType = ""
    is_editing: bool = False
    editing_id: int | None = None
    teacher_name: str = ""
    teacher_email: str = ""
    class_name: str = ""
    class_subject: str = ""
    class_duration: str = "60"
    schedule_class_id: str = ""
    schedule_teacher_id: str = ""
    schedule_day_of_week: str = "Monday"
    schedule_start_time: str = "09:00"
    rule_teacher_id: str = ""
    rule_min_hours: str = ""
    _next_teacher_id: int = 4
    _next_class_id: int = 4
    _next_schedule_id: int = 1
    _next_rule_id: int = 3

    @rx.var
    def current_page(self) -> str:
        return self.router.page.path.strip("/") or "dashboard"

    @rx.var
    def teacher_hours(self) -> dict[int, float]:
        hours = {teacher["id"]: 0 for teacher in self.teachers}
        class_durations = {c["id"]: c["duration"] for c in self.classes}
        for schedule in self.schedules:
            duration = class_durations.get(schedule["class_id"], 0)
            hours[schedule["teacher_id"]] += duration / 60
        return hours

    @rx.var
    def teacher_rules(self) -> dict[int, int]:
        return {rule["teacher_id"]: rule["min_hours"] for rule in self.rules}

    @rx.var
    def rule_compliance(self) -> float:
        compliant_teachers = 0
        total_teachers_with_rules = 0
        teacher_hours = self.teacher_hours
        teacher_rules = self.teacher_rules
        for teacher_id, min_hours in teacher_rules.items():
            total_teachers_with_rules += 1
            if teacher_hours.get(teacher_id, 0) >= min_hours:
                compliant_teachers += 1
        if total_teachers_with_rules == 0:
            return 100.0
        return compliant_teachers / total_teachers_with_rules * 100

    def _create_teacher(self):
        new_teacher: Teacher = {
            "id": self._next_teacher_id,
            "name": self.teacher_name,
            "email": self.teacher_email,
        }
        self.teachers.append(new_teacher)
        self._next_teacher_id += 1

    def _update_teacher(self):
        if self.editing_id is not None:
            for i, teacher in enumerate(self.teachers):
                if teacher["id"] == self.editing_id:
                    self.teachers[i]["name"] = self.teacher_name
                    self.teachers[i]["email"] = self.teacher_email
                    break

    @rx.event
    def save_teacher(self):
        if self.is_editing:
            self._update_teacher()
        else:
            self._create_teacher()
        yield State.close_modal()

    @rx.event
    def delete_teacher(self, teacher_id: int):
        self.teachers = [t for t in self.teachers if t["id"] != teacher_id]

    def _create_class(self):
        new_class: Class = {
            "id": self._next_class_id,
            "name": self.class_name,
            "subject": self.class_subject,
            "duration": int(self.class_duration),
        }
        self.classes.append(new_class)
        self._next_class_id += 1

    def _update_class(self):
        if self.editing_id is not None:
            for i, c in enumerate(self.classes):
                if c["id"] == self.editing_id:
                    self.classes[i]["name"] = self.class_name
                    self.classes[i]["subject"] = self.class_subject
                    self.classes[i]["duration"] = int(self.class_duration)
                    break

    @rx.event
    def save_class(self):
        if self.is_editing:
            self._update_class()
        else:
            self._create_class()
        yield State.close_modal()

    @rx.event
    def delete_class(self, class_id: int):
        self.classes = [c for c in self.classes if c["id"] != class_id]

    def _create_rule(self):
        new_rule: Rule = {
            "id": self._next_rule_id,
            "teacher_id": int(self.rule_teacher_id),
            "min_hours": int(self.rule_min_hours),
        }
        self.rules.append(new_rule)
        self._next_rule_id += 1

    def _update_rule(self):
        if self.editing_id is not None:
            for i, rule in enumerate(self.rules):
                if rule["id"] == self.editing_id:
                    self.rules[i]["teacher_id"] = int(self.rule_teacher_id)
                    self.rules[i]["min_hours"] = int(self.rule_min_hours)
                    break

    @rx.event
    def save_rule(self):
        if not self.rule_teacher_id or not self.rule_min_hours:
            return rx.toast("Please select a teacher and set minimum hours.")
        if self.is_editing:
            self._update_rule()
        else:
            self._create_rule()
        yield State.close_modal()

    @rx.event
    def delete_rule(self, rule_id: int):
        self.rules = [r for r in self.rules if r["id"] != rule_id]

    def _calculate_end_time(self, start_time: str, duration_minutes: int) -> str:
        from datetime import datetime, timedelta

        start_dt = datetime.strptime(start_time, "%H:%M")
        end_dt = start_dt + timedelta(minutes=duration_minutes)
        return end_dt.strftime("%H:%M")

    def _check_conflict(
        self,
        new_start_str: str,
        new_end_str: str,
        teacher_id: int,
        day: str,
        exclude_schedule_id: int | None = None,
    ) -> bool:
        from datetime import datetime

        new_start = datetime.strptime(new_start_str, "%H:%M").time()
        new_end = datetime.strptime(new_end_str, "%H:%M").time()
        for schedule in self.schedules:
            if schedule["id"] == exclude_schedule_id:
                continue
            if schedule["teacher_id"] == teacher_id and schedule["day_of_week"] == day:
                existing_start = datetime.strptime(
                    schedule["start_time"], "%H:%M"
                ).time()
                existing_end = datetime.strptime(schedule["end_time"], "%H:%M").time()
                if new_start < existing_end and new_end > existing_start:
                    return True
        return False

    def _create_schedule(self):
        class_id = int(self.schedule_class_id)
        teacher_id = int(self.schedule_teacher_id)
        selected_class = next((c for c in self.classes if c["id"] == class_id), None)
        if not selected_class:
            return rx.toast("Selected class not found.")
        end_time = self._calculate_end_time(
            self.schedule_start_time, selected_class["duration"]
        )
        if self._check_conflict(
            self.schedule_start_time, end_time, teacher_id, self.schedule_day_of_week
        ):
            return rx.toast(
                "Schedule conflict: Teacher is already booked at this time.",
                duration=5000,
            )
        new_schedule: Schedule = {
            "id": self._next_schedule_id,
            "class_id": class_id,
            "teacher_id": teacher_id,
            "day_of_week": self.schedule_day_of_week,
            "start_time": self.schedule_start_time,
            "end_time": end_time,
        }
        self.schedules.append(new_schedule)
        self._next_schedule_id += 1
        return State.close_modal()

    def _update_schedule(self):
        if self.editing_id is not None:
            class_id = int(self.schedule_class_id)
            teacher_id = int(self.schedule_teacher_id)
            selected_class = next(
                (c for c in self.classes if c["id"] == class_id), None
            )
            if not selected_class:
                return rx.toast("Selected class not found.")
            end_time = self._calculate_end_time(
                self.schedule_start_time, selected_class["duration"]
            )
            if self._check_conflict(
                self.schedule_start_time,
                end_time,
                teacher_id,
                self.schedule_day_of_week,
                exclude_schedule_id=self.editing_id,
            ):
                return rx.toast(
                    "Schedule conflict: Teacher is already booked at this time.",
                    duration=5000,
                )
            for i, schedule in enumerate(self.schedules):
                if schedule["id"] == self.editing_id:
                    self.schedules[i]["class_id"] = class_id
                    self.schedules[i]["teacher_id"] = teacher_id
                    self.schedules[i]["day_of_week"] = self.schedule_day_of_week
                    self.schedules[i]["start_time"] = self.schedule_start_time
                    self.schedules[i]["end_time"] = end_time
                    break
            return State.close_modal()

    @rx.event
    def save_schedule(self):
        if not self.schedule_class_id or not self.schedule_teacher_id:
            return rx.toast("Please select both a class and a teacher.")
        if self.is_editing:
            return self._update_schedule()
        else:
            return self._create_schedule()

    @rx.event
    def delete_schedule(self, schedule_id: int):
        self.schedules = [s for s in self.schedules if s["id"] != schedule_id]

    def _reset_form_fields(self):
        self.teacher_name = ""
        self.teacher_email = ""
        self.class_name = ""
        self.class_subject = ""
        self.class_duration = "60"
        self.schedule_class_id = ""
        self.schedule_teacher_id = ""
        self.schedule_day_of_week = "Monday"
        self.schedule_start_time = "09:00"
        self.rule_teacher_id = ""
        self.rule_min_hours = ""
        self.editing_id = None
        self.is_editing = False

    @rx.event
    def open_modal(self, modal_type: ModalType, item_id: int | None = None):
        self.modal_type = modal_type
        self.show_modal = True
        self._reset_form_fields()
        if item_id is not None:
            self.is_editing = True
            self.editing_id = item_id
            if modal_type == "teacher":
                teacher = next((t for t in self.teachers if t["id"] == item_id), None)
                if teacher:
                    self.teacher_name = teacher["name"]
                    self.teacher_email = teacher["email"]
            elif modal_type == "class":
                _class = next((c for c in self.classes if c["id"] == item_id), None)
                if _class:
                    self.class_name = _class["name"]
                    self.class_subject = _class["subject"]
                    self.class_duration = str(_class["duration"])
            elif modal_type == "schedule":
                schedule = next((s for s in self.schedules if s["id"] == item_id), None)
                if schedule:
                    self.schedule_class_id = str(schedule["class_id"])
                    self.schedule_teacher_id = str(schedule["teacher_id"])
                    self.schedule_day_of_week = schedule["day_of_week"]
                    self.schedule_start_time = schedule["start_time"]
            elif modal_type == "rule":
                rule = next((r for r in self.rules if r["id"] == item_id), None)
                if rule:
                    self.rule_teacher_id = str(rule["teacher_id"])
                    self.rule_min_hours = str(rule["min_hours"])

    @rx.event
    def close_modal(self):
        self.show_modal = False
        self.modal_type = ""
        self._reset_form_fields()