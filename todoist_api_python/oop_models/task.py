from todoist_api_python.oop_models.base import TodoistObject
from todoist_api_python._core.endpoints import get_task_url
from todoist_api_python._core.utils import log_method_calls

@log_method_calls(exclude_private=True, exclude_dunder=True) # Log calls to any method except dunders, private, and properties
class Task(TodoistObject):
    _data       = property( lambda self : self.env._get_task_data_by_id(self._id) )

    #################################################################
    #
    # Immutable properties
    #
    #################################################################
    url          = property( lambda self : get_task_url(self._id,self.content) )
    added_at     = property( lambda self : self._data.added_at     )
    updated_at   = property( lambda self : self._data.updated_at   )
    completed_at = property( lambda self : self._data.completed_at )

    #################################################################
    #
    # Basic properties accessible via update_task
    #
    #################################################################
    content     = property( lambda self : self._data.content     )
    description = property( lambda self : self._data.description )
    priority    = property( lambda self : self._data.priority    )

    def _update_task(self, **kwargs) -> None:
        # Update task attributes via the API
        # attaches the ID and forwards kwargs to the API method
        self.env._update_task(self, **kwargs)

    def set_content(self, new_content) -> None:
        self._update_task(content=new_content)

    def set_description(self, new_description) -> None:
        self._update_task(description=new_description)

    # TODO handle labels? they're a bit strange because
    # they get returned from the API as names, but we
    # would prefer to work with OBJECTS and we can only
    # get an object from an ID, not a name
    # def add_label(self, label):
    # def remove_label(self, label):
    # def has_label(self, label):

    def set_priority(self, new_priority) -> None:
        self._update_task(priority=new_priority)

    # TODO handle due dates
    # the way they are stored is a bit opaque to me
    # just need to figure that out and be able to set them
    # might want a few set methods for natural language or
    # specific date formats

    # TODO support deadlines and durations too

    #################################################################
    #
    # Subtasks
    #
    #################################################################
    def add_subtask(self, **kwargs) -> "Task":
        return self.env._add_task(parent=self, **kwargs)

    def get_subtasks(self) -> list["Task"]:
        return self.env._get_tasks(parent=self)

    is_subtask = property( lambda self : self._data.parent_id is not None )

    #################################################################
    #
    # Status
    #
    #################################################################
    def mark_complete(self) -> None:
        self.env._complete_task(self)

    def unmark_complete(self) -> None:
        self.env._uncomplete_task(self)

    is_complete = property( lambda self : self._data.completed_at is not None )

    #################################################################
    #
    # Delete and manage hierarchy
    #
    #################################################################
    def delete(self) -> None:
        self.env._delete_task(self)
        self._id = None

    def move(self, new_parent) -> None:
        self.env._move_task(self, new_parent)

    def get_project(self) -> "Project":
        return self.env._get_project_by_id(self._data.project_id)

    def get_section(self) -> "Section | None":
        if (section_id := self._data.section_id) is None:
            return None
        else:
            return self.env._get_section_by_id(section_id)

    def get_parent_task(self) -> "Task | None":
        if (parent_id := self._data.parent_id) is None:
            return None
        else:
            return self.env._get_task_by_id(parent_id)

    def get_parent(self) -> "Task | Section | Project":
        return self.get_parent_task() or self.get_section() or self.get_project()

    #################################################################
    #
    # Comments
    #
    #################################################################
    def add_comment(self, **kwargs) -> "Comment":
        return self.env._add_comment(task=self, **kwargs)

    def get_comments(self) -> list["Comment"]:
        return self.env._get_comments(task=self)
