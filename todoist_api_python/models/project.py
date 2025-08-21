from .ABC import TodoistObject
from typing import Any

class Project(TodoistObject):
    def _extract_values(self, raw_data: dict[str, Any]):
        self.name = raw_data.pop("name")

    @classmethod
    def create_new(cls, api, name): # TODO don't pass in API, instead use a singleton
        response = api.add_project(
            name=name
            # Add other properties as needed
        )
        return response

    def _push_updates(self, api):
        api.update_project(
            project_id=self._id,
            name=self.name,
            # Add other properties as needed
        )

    def delete(self, api): # TODO change to singleton API
        """
        Delete this item.
        """
        api.delete_project(self._id)
        # TODO handle errors, e.g. if the item is already deleted
        # TODO do not allow further edits after deletion
        # TODO remove the item from the container
