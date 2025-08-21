from .ABC import TodoistObject
from typing import Any

class Project(TodoistObject):
    def _extract_values(self, raw_data: dict[str, Any]):
        self.name = raw_data.pop("name")

    def _push_updates(self):
        self._env.api.update_project(
            project_id=self._id,
            name=self.name,
            # Add other properties as needed
        )

    def delete(self): # TODO change to singleton API
        """
        Delete this item.
        """
        self._env.api.delete_project(self._id)
        # TODO handle errors, e.g. if the item is already deleted
        # TODO do not allow further edits after deletion
        # TODO remove the item from the container

    @property
    def tasks(self):
        """
        Get all tasks in this project.
        """
        return filter(self._env.tasks, lambda task: task.project == self)
