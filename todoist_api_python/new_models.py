from typing import Any
from abc import ABC, abstractmethod

class TodoistObject(ABC):
    @classmethod
    def from_dict(cls, raw_data: dict[str, Any]):
        """
        Create an instance of the class from a dictionary.
        This method should be overridden by subclasses to handle specific initialization.
        """
        return cls(raw_data)

    @classmethod
    @abstractmethod
    def create_new(cls, api, name): # TODO don't pass in API, instead use a singleton
        raise NotImplementedError("Create new method not implemented. Please implement this method in your subclass.")

    @abstractmethod
    def push_updates(self, api):
        """
        Push updates to this item to the Todoist API.
        Does not check if the item has been modified.
        TODO check if the item has been modified before pushing updates.
        """
        raise NotImplementedError("Push updates method not implemented. Please implement this method in your subclass.")

    @abstractmethod
    def delete(self, api):
        """
        Delete this item.
        """
        raise NotImplementedError("Delete method not implemented. Please implement this method in your subclass.")

class Project(TodoistObject):
    def __init__(self, raw_data : dict[str,Any]):
        """
        raw_data is a dictionary received directly from the API
        It has the following keys: access, can_assign_tasks, child_order, color, created_at, creator_uid, default_order, description, id, is_archived, is_collapsed, is_deleted, is_favorite, is_frozen, is_shared, name, parent_id, public_access, public_key, role, updated_at, view_style

        A 'useful' selection of these keys are handled in the method below

        The remaining keys are stored immutably for reference
        Accessing these keys yields a warning
        If you find yourself accessing these keys, please consider forking this package and writing proper getter/setters for them.
        """
        # Properties reflected in the API interactions
        self.name = raw_data.pop("name")
        self._id = raw_data.pop("id")
        # Add other properties as needed
        self._other_data = raw_data # Included only in case of emergency, and for debugging purposes

    @classmethod
    def create_new(cls, api, name): # TODO don't pass in API, instead use a singleton
        response = api.add_project(
            name=name
            # Add other properties as needed
        )
        return response

    def push_updates(self, api):
        """
        Push updates to this item to the Todoist API.
        Does not check if the item has been modified.
        TODO check if the item has been modified before pushing updates.
        """
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

class Section(TodoistObject):
    def __init__(self, raw_data : dict[str,Any]):
        """
        raw_data is a dictionary received directly from the API
        It has the following keys: access, can_assign_tasks, child_order, color, created_at, creator_uid, default_order, description, id, is_archived, is_collapsed, is_deleted, is_favorite, is_frozen, is_shared, name, parent_id, public_access, public_key, role, updated_at, view_style

        A 'useful' selection of these keys are handled in the method below

        The remaining keys are stored immutably for reference
        Accessing these keys yields a warning
        If you find yourself accessing these keys, please consider forking this package and writing proper getter/setters for them.
        """
        # Properties reflected in the API interactions
        self.name = raw_data.pop("name")
        self._id = raw_data.pop("id")
        # Add other properties as needed
        self._other_data = raw_data # Included only in case of emergency, and for debugging purposes

    @classmethod
    def create_new(cls, api, name): # TODO don't pass in API, instead use a singleton
        response = api.add_section(
            name=name
            # Add other properties as needed
        )
        return response

    def push_updates(self, api):
        """
        Push updates to this item to the Todoist API.
        Does not check if the item has been modified.
        TODO check if the item has been modified before pushing updates.
        """
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

class Task(TodoistObject):
    def __init__(self, raw_data : dict[str,Any]):
        """
        raw_data is a dictionary received directly from the API
        It has the following keys: access, can_assign_tasks, child_order, color, created_at, creator_uid, default_order, description, id, is_archived, is_collapsed, is_deleted, is_favorite, is_frozen, is_shared, name, parent_id, public_access, public_key, role, updated_at, view_style

        A 'useful' selection of these keys are handled in the method below

        The remaining keys are stored immutably for reference
        Accessing these keys yields a warning
        If you find yourself accessing these keys, please consider forking this package and writing proper getter/setters for them.
        """
        # Properties reflected in the API interactions
        self.content = raw_data.pop("content")
        self._id = raw_data.pop("id")
        # Add other properties as needed
        self._other_data = raw_data # Included only in case of emergency, and for debugging purposes

    @classmethod
    def create_new(cls, api, content): # TODO don't pass in API, instead use a singleton
        response = api.add_task(
            content=content
            # Add other properties as needed
        )
        return response

    def push_updates(self, api):
        """
        Push updates to this item to the Todoist API.
        Does not check if the item has been modified.
        TODO check if the item has been modified before pushing updates.
        """
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

class Label(TodoistObject):
    def __init__(self, raw_data : dict[str,Any]):
        """
        raw_data is a dictionary received directly from the API
        It has the following keys: access, can_assign_tasks, child_order, color, created_at, creator_uid, default_order, description, id, is_archived, is_collapsed, is_deleted, is_favorite, is_frozen, is_shared, name, parent_id, public_access, public_key, role, updated_at, view_style

        A 'useful' selection of these keys are handled in the method below

        The remaining keys are stored immutably for reference
        Accessing these keys yields a warning
        If you find yourself accessing these keys, please consider forking this package and writing proper getter/setters for them.
        """
        # Properties reflected in the API interactions
        self.name = raw_data.pop("name")
        self._id = raw_data.pop("id")
        # Add other properties as needed
        self._other_data = raw_data # Included only in case of emergency, and for debugging purposes

    @classmethod
    def create_new(cls, api, name): # TODO don't pass in API, instead use a singleton
        response = api.add_label(
            name=name
            # Add other properties as needed
        )
        return response

    def push_updates(self, api):
        """
        Push updates to this item to the Todoist API.
        Does not check if the item has been modified.
        TODO check if the item has been modified before pushing updates.
        """
        api.update_label(
            label_id=self._id,
            name=self.name,
            # Add other properties as needed
        )

    def delete(self, api):
        """
        Delete this item.
        """
        api.delete_label(self._id)

class Comment(TodoistObject):
    def __init__(self, raw_data : dict[str,Any]):
        """
        raw_data is a dictionary received directly from the API
        It has the following keys: access, can_assign_tasks, child_order, color, created_at, creator_uid, default_order, description, id, is_archived, is_collapsed, is_deleted, is_favorite, is_frozen, is_shared, name, parent_id, public_access, public_key, role, updated_at, view_style

        A 'useful' selection of these keys are handled in the method below

        The remaining keys are stored immutably for reference
        Accessing these keys yields a warning
        If you find yourself accessing these keys, please consider forking this package and writing proper getter/setters for them.
        """
        # Properties reflected in the API interactions
        self.name = raw_data.pop("name")
        self._id = raw_data.pop("id")
        # Add other properties as needed
        self._other_data = raw_data # Included only in case of emergency, and for debugging purposes

    @classmethod
    def create_new(cls, api, name): # TODO don't pass in API, instead use a singleton
        response = api.add_comment(
            name=name
            # Add other properties as needed
        )
        return response

    def push_updates(self, api):
        """
        Push updates to this item to the Todoist API.
        Does not check if the item has been modified.
        TODO check if the item has been modified before pushing updates.
        """
        api.update_comment(
            comment_id=self._id,
            name=self.name,
            # Add other properties as needed
        )

    def delete(self, api):
        """
        Delete this item.
        """
        api.delete_comment(self._id)
