from .ABC import TodoistObject
from typing import Any

class Section(TodoistObject):
    def _extract_values(self, raw_data: dict[str, Any]):
        self.name = raw_data.pop("name")

    def _push_updates(self):
        self._env.api.update_section(
            section_id=self._id,
            name=self.name,
            # Add other properties as needed
        )

    def delete(self):
        """
        Delete this item.
        """
        self._env.api.delete_section(self._id)
