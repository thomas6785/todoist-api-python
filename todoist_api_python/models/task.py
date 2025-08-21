from .ABC import TodoistObject
from typing import Any

class Task(TodoistObject):
    def _extract_values(self, raw_data: dict[str, Any]):
        self.content = raw_data.pop("content")
        self.project = [ project for project in self._env.projects if project._id == raw_data.pop("project_id") ][0]

    def _push_updates(self):
        self._env.api.update_task(
            task_id=self._id,
            content=self.content,
            # Add other properties as needed
        )

    def delete(self):
        """
        Delete this item.
        """
        self._env.api.delete_task(self._id)
