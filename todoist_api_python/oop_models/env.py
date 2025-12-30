"""
Todoist Env is the main entry point for manipulating Todoist objects using OOP models

It is a wrapper around an API object
It is HIGHLY recommended this be an API object WITH CACHING
as the OOP models make VERY liberal use of API calls, even for
simple property accesses.

It provides methods in three categories:
- API wrapper methods
    These are analogues of the API methods, but their signatures are
    modified to take in objects instead of ID's, and return objects
    Paginated results are flattened into a single list of objects

    These should not be used by the user

- Special ID getters
    These get objects by ID, returning the appropriate OOP model object

- Data getters
    These get a dataclass object from the core API by ID
    These are used internally by the OOP models to get their data

- User-facing methods
    The only public methods
"""

from todoist_api_python.oop_models.task import Task
from todoist_api_python.oop_models.project import Project
from todoist_api_python.oop_models.section import Section
from todoist_api_python.oop_models.label import Label
from todoist_api_python.oop_models.comment import Comment

# Decorator to wrap an API method with the first argument as an object ID (e.g. update_task)
# Not all API methods can be wrapped this way
def wrap_api_method(func):
    @wraps(func)
    def wrapped_method(self,obj,*args,**kwargs):
        obj_id = obj._id # e.g. extract task ID from a Task object
        func(obj_id,*args,**kwargs)
    return wrapped_method

# TODO consider splitting this up into several objects
# it's kind of a monolith and serving a few different purposes
class TodoistEnv:
    def __init__(self, api):
        self._api = api

    def __enter__(self): return self._api.__enter__()
    def __exit__(self, *args, **kwargs): return self._api.__exit__(*args,**kwargs)

    ############################################
    #
    # API getters by ID
    # Return a dataclass from the API core
    #
    ############################################
    def _get_task_data_by_id(self, task_id):
        return self._api.get_task(task_id)

    def _get_project_data_by_id(self, project_id):
        return self._api.get_project(project_id)

    def _get_label_data_by_id(self, label_id):
        return self._api.get_label(label_id)

    def _get_comment_data_by_id(self, comment_id):
        return self._api.get_comment(comment_id)

    def _get_section_data_by_id(self, section_id):
        return self._api.get_section(section_id)

    # The OOP models need to know the env, so we can just forward 'self' and the ID
    def _get_task_by_id(self, _id):    return Task(_id, self)
    def _get_project_by_id(self, _id): return Project(_id, self)
    def _get_section_by_id(self, _id): return Section(_id, self)
    def _get_label_by_id(self, _id):   return Label(_id, self)
    def _get_comment_by_id(self, _id): return Comment(_id, self)
    # fuck off Pylint it looks cleaner this way

    ############################################
    #
    # API wrapper methods
    #
    ############################################
    self._update_task       = wrap_api_method( self._api.update_task            )
    self._update_project    = wrap_api_method( self._api.update_project         )
    self._update_comment    = wrap_api_method( self._api.update_comment         )
    self._update_label      = wrap_api_method( self._api.update_label           )
    self._update_section    = wrap_api_method( self._api.update_section         )
    self._complete_task     = wrap_api_method( self._api.complete_task          )
    self._uncomplete_task   = wrap_api_method( self._api.uncomplete_task        )
    self._archive_project   = wrap_api_method( self._api.archive_project        )
    self._unarchive_project = wrap_api_method( self._api.unarchive_project      )
    