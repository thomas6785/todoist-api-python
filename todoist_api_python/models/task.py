from .ABC import TodoistObject
from typing import Any

class Task(TodoistObject):
    def _extract_values(self, raw_data: dict[str, Any]):
        self.content = raw_data.pop("content")

    @classmethod
    def create_new(cls, api, content): # TODO don't pass in API, instead use a singleton
        response = api.add_task(
            content=content
            # Add other properties as needed
        )
        return response

    def _push_updates(self, api):
        api.update_task(
            task_id=self._id,
            content=self.content,
            # Add other properties as needed
        )

    def delete(self, api):
        """
        Delete this item.
        """
        api.delete_task(self._id)
