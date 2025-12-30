from todoist_api_python.oop_models.base import TodoistObject
from todoist_api_python._core.utils import log_method_calls

@log_method_calls(exclude_private=True, exclude_dunder=True) # Log calls to any method except dunders and private
class Section(TodoistObject):
    _data       = property( lambda self : self.env._get_section_data_by_id(self._id) )
