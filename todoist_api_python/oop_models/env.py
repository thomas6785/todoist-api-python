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

class TodoistEnv:
    def __init__(self, api):
        self._api = api

    def __enter__(self): return self._api.__enter__()
    def __exit__(self, *args, **kwargs): return self._api.__exit__(*args,**kwargs)

    def _get_task_data_by_id(self, task_id):
        return self._api.get_task(task_id)
        # returns a dataclass from the core API
