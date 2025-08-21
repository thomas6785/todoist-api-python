from .ABC import TodoistObject
from typing import Any

class Section(TodoistObject):
    def _extract_values(self, raw_data: dict[str, Any]):
        self.name = raw_data.pop("name")

    @classmethod
    def create_new(cls, api, name): # TODO don't pass in API, instead use a singleton
        response = api.add_section(
            name=name
            # Add other properties as needed
        )
        return response

    def _push_updates(self, api):
        api.update_section(
            section_id=self._id,
            name=self.name,
            # Add other properties as needed
        )

    def delete(self, api):
        """
        Delete this item.
        """
        api.delete_section(self._id)
