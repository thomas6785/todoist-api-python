from typing import Any
from abc import ABC, abstractmethod

class TodoistObject(ABC):
    def __init__(self, raw_data : dict[str,Any], env : "TodoistEnv"):
        """
        raw_data is a dictionary received directly from the API
        It has the following keys: access, can_assign_tasks, child_order, color, created_at, creator_uid, default_order, description, id, is_archived, is_collapsed, is_deleted, is_favorite, is_frozen, is_shared, name, parent_id, public_access, public_key, role, updated_at, view_style

        A 'useful' selection of these keys are handled in the method below

        The remaining keys are stored immutably for reference
        Accessing these keys yields a warning
        If you find yourself accessing these keys, please consider forking this package and writing proper getter/setters for them.
        """
        self._id = raw_data.pop("id")
        self._env = env

        # Properties reflected in the API interactions
        self._extract_values(raw_data)

        # Add other properties as needed
        self._other_data = raw_data # Included only in case of emergency, and for debugging purposes

        self._modified = False

    @classmethod
    def from_dict(cls, raw_data: dict[str, Any]):
        """
        Create an instance of the class from a dictionary.
        This method should be overridden by subclasses to handle specific initialization.
        """
        return cls(raw_data)

    @abstractmethod
    def delete(self):
        """
        Delete this item.
        """
        raise NotImplementedError("Delete method not implemented. Please implement this method in your subclass.")

    def __setattr__(self, key, value):
        if key != "_modified":
            self._modified = True
        super().__setattr__(key, value)

    @abstractmethod
    def _extract_values(self, raw_data: dict[str, Any]):
        raise NotImplementedError("This method should be overridden by subclasses to extract specific values from raw_data.")

    def push_updates(self):
        """
        Push updates to this item to the Todoist API.
        Checks if the item has been modified then calls _push_updates.
        If the item has not been modified, no API call is made.
        """
        if self._modified:
            self._push_updates()
            self._modified = False

    @abstractmethod
    def _push_updates(self):
        """
        Internal method to push updates to the API.
        This is a placeholder and should be implemented in subclasses.
        """
        raise NotImplementedError("This method should be overridden by subclasses to handle API updates.")