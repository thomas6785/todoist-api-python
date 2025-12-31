import logging
from typing import Callable, Iterable
from functools import wraps

from todoist_api_python.api import TodoistAPI

logger = logging.getLogger(__name__)

# Utility to make function arguments hashable as a key for caching
def make_args_hashable(args : tuple, kwargs : dict):
    # TODO research the best practice for doing this
    # for now we are making a big tuple
    return args + tuple(sorted(kwargs.items()))
    # we sort the kwargs because the order should be irrelevant (dict should be unordered anyway, but Python sometimes retains the order for some reason?)

# Decorator to cache function return values
# Provides methods to clear the cache, invalidate a specific entry, and force a specific entry
def cached(func):
    logger.debug(f"Initialising cache for {func}")
    func._cached_values = {}
    func._cache_hits = 0
    func._cache_misses = 0
    @wraps(func)
    def wrapped_function(*args,**kwargs):
        key = make_args_hashable(args,kwargs)
        if key in func._cached_values:
            logger.debug(f"Cache hit on {func} for args {key}. Returning cached value")
            func._cache_hits += 1
            return func._cached_values[key]
        else:
            logger.debug(f"Cache miss on {func} for args {key}. Calling function")
            func._cache_misses += 1
            result = func(*args,**kwargs)
            func._cached_values[key] = result
            return result
    
    def cache_clear():
        logger.debug(f"Cache on {func} was cleared")
        func._cached_values = {}
    
    def invalidate_cache_entry(key):
        if key in func._cached_values:
            logger.debug(f"Cache on {func} had this key invalidate: {key}")
            del func._cached_values[key]
        else:
            logger.debug(f"Cache on {func} key to invalidate was not found. Key: {key}")

    def force_cache_entry(key, value):
        logger.debug(f"Cache on {func} had this key forced: {key}")
        func._cached_values[key] = value

    wrapped_function.cache_clear = cache_clear
    wrapped_function.invalidate_cache_entry = invalidate_cache_entry
    return wrapped_function

# Decorator to clear caches on other methods when this method is called
# TODO convert to a decorator that supports @ syntactic sugar e.g. @invalidates_caches(...)
def cache_invalidator(method, cached_methods_to_invalidate):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        for cached_method in cached_methods_to_invalidate:
            cached_method.cache_clear()
        return result
    return wrapper

# Decorator to convert paginated results into a list
def capture_list(method : Callable[...,Iterable[list]]):
    @wraps(method)
    def wrapper(*args, **kwargs) -> list[list]:
        result = method(*args, **kwargs)
        return list(result)
    return wrapper

class CachedTodoistAPI(TodoistAPI):
    """
    Wrapper for the Todoist API client with caching on 'get' methods.

    Note paginated results are returned as a 2D list instead of an iterator of lists.
    This is to accommodate caching.
    """
    # TODO implement much smarter cache invalidation by only invalidating caches that are relevant to the data that was changed
    # There are only two hard things in computer science: cache invalidation and naming things - Phil Karlton

    ##################################################################################
    #
    # All 'get' methods can be cached
    #
    ##################################################################################
    get_task                                = cached(               TodoistAPI.get_task                                 )
    get_tasks                               = cached( capture_list( TodoistAPI.get_tasks                              ) )
    filter_tasks                            = cached( capture_list( TodoistAPI.filter_tasks                           ) )
    get_completed_tasks_by_due_date         = cached( capture_list( TodoistAPI.get_completed_tasks_by_due_date        ) )
    get_completed_tasks_by_completion_date  = cached( capture_list( TodoistAPI.get_completed_tasks_by_completion_date ) )
    get_project                             = cached(               TodoistAPI.get_project                              )
    get_projects                            = cached( capture_list( TodoistAPI.get_projects                           ) )
    get_collaborators                       = cached( capture_list( TodoistAPI.get_collaborators                      ) )
    get_section                             = cached(               TodoistAPI.get_section                              )
    get_sections                            = cached( capture_list( TodoistAPI.get_sections                           ) )
    get_comment                             = cached(               TodoistAPI.get_comment                              )
    get_comments                            = cached( capture_list( TodoistAPI.get_comments                           ) )
    get_label                               = cached(               TodoistAPI.get_label                                )
    get_labels                              = cached( capture_list( TodoistAPI.get_labels                             ) )
    get_shared_labels                       = cached( capture_list( TodoistAPI.get_shared_labels                      ) )
    # capture_list will convert a PagintedResults object into a list
    # this means that the return type is now List[dict[str,Any]] instead of Iterator[dict[str,Any]]
    # it will cache better this way, but is expensive for large result sets

    ##################################################################################
    #
    # 'set' methods need to be wrapped to invalidate the relevant caches
    #
    ##################################################################################

    # TODO be smarter and only invalidate the caches for methods where it is relevant, e.g. get_task(task_id) only needs to be invalidated for that task_id
    # This is a little complicated when it comes to things like get_tasks(project_id)
    # For now, we will zealously invalidate any vaguely relevant cache as below:
    HIGHLY_SENSITIVE_CACHES = {filter_tasks, get_completed_tasks_by_completion_date, get_completed_tasks_by_due_date} # always clear this cache because the filter queries can select for pretty much anything

    TASK_SENSITIVE_CACHES    = HIGHLY_SENSITIVE_CACHES | {get_task, get_tasks}
    SECTION_SENSITIVE_CACHES = HIGHLY_SENSITIVE_CACHES | {get_section, get_sections}
    PROJECT_SENSITIVE_CACHES = HIGHLY_SENSITIVE_CACHES | {get_project, get_projects}
    LABEL_SENSITIVE_CACHES   = HIGHLY_SENSITIVE_CACHES | {get_labels, get_label, get_shared_labels}
    COMMENT_SENSITIVE_CACHES = HIGHLY_SENSITIVE_CACHES | {get_comment, get_comments}
    ALL_CACHES               = TASK_SENSITIVE_CACHES | SECTION_SENSITIVE_CACHES | PROJECT_SENSITIVE_CACHES | LABEL_SENSITIVE_CACHES | COMMENT_SENSITIVE_CACHES

    ###############################################
    # Task manipulators
    ###############################################
    add_task                                = cache_invalidator(TodoistAPI.add_task,         ALL_CACHES | TASK_SENSITIVE_CACHES)
    add_task_quick                          = cache_invalidator(TodoistAPI.add_task_quick,   ALL_CACHES | TASK_SENSITIVE_CACHES)
    update_task                             = cache_invalidator(TodoistAPI.update_task,      ALL_CACHES | TASK_SENSITIVE_CACHES)
    complete_task                           = cache_invalidator(TodoistAPI.complete_task,    ALL_CACHES | TASK_SENSITIVE_CACHES)
    uncomplete_task                         = cache_invalidator(TodoistAPI.uncomplete_task,  ALL_CACHES | TASK_SENSITIVE_CACHES)
    move_task                               = cache_invalidator(TodoistAPI.move_task,        ALL_CACHES | TASK_SENSITIVE_CACHES)
    delete_task                             = cache_invalidator(TodoistAPI.delete_task,      ALL_CACHES | TASK_SENSITIVE_CACHES | COMMENT_SENSITIVE_CACHES | LABEL_SENSITIVE_CACHES)

    ###############################################
    # Section manipulators
    ###############################################
    add_section                             = cache_invalidator(TodoistAPI.add_section,       ALL_CACHES | SECTION_SENSITIVE_CACHES)
    update_section                          = cache_invalidator(TodoistAPI.update_section,    ALL_CACHES | SECTION_SENSITIVE_CACHES)
    delete_section                          = cache_invalidator(TodoistAPI.delete_section,    ALL_CACHES | SECTION_SENSITIVE_CACHES | TASK_SENSITIVE_CACHES | COMMENT_SENSITIVE_CACHES | LABEL_SENSITIVE_CACHES)

    ###############################################
    # Project manipulators
    ###############################################
    add_project                             = cache_invalidator(TodoistAPI.add_project,       ALL_CACHES | PROJECT_SENSITIVE_CACHES)
    update_project                          = cache_invalidator(TodoistAPI.update_project,    ALL_CACHES | PROJECT_SENSITIVE_CACHES)
    archive_project                         = cache_invalidator(TodoistAPI.archive_project,   ALL_CACHES | PROJECT_SENSITIVE_CACHES)
    unarchive_project                       = cache_invalidator(TodoistAPI.unarchive_project, ALL_CACHES | PROJECT_SENSITIVE_CACHES)
    delete_project                          = cache_invalidator(TodoistAPI.delete_project,    ALL_CACHES | PROJECT_SENSITIVE_CACHES | SECTION_SENSITIVE_CACHES | TASK_SENSITIVE_CACHES | COMMENT_SENSITIVE_CACHES | LABEL_SENSITIVE_CACHES)

    ###############################################
    # Comment manipulators
    ###############################################
    add_comment                             = cache_invalidator(TodoistAPI.add_comment,      ALL_CACHES | COMMENT_SENSITIVE_CACHES)
    update_comment                          = cache_invalidator(TodoistAPI.update_comment,   ALL_CACHES | COMMENT_SENSITIVE_CACHES)
    delete_comment                          = cache_invalidator(TodoistAPI.delete_comment,   ALL_CACHES | COMMENT_SENSITIVE_CACHES)

    ###############################################
    # Label manipulators
    ###############################################
    add_label                               = cache_invalidator(TodoistAPI.add_label,              ALL_CACHES | LABEL_SENSITIVE_CACHES)
    update_label                            = cache_invalidator(TodoistAPI.update_label,           ALL_CACHES | LABEL_SENSITIVE_CACHES)
    delete_label                            = cache_invalidator(TodoistAPI.delete_label,           ALL_CACHES | LABEL_SENSITIVE_CACHES)
    rename_shared_label                     = cache_invalidator(TodoistAPI.rename_shared_label,    ALL_CACHES | LABEL_SENSITIVE_CACHES)
    remove_shared_label                     = cache_invalidator(TodoistAPI.remove_shared_label,    ALL_CACHES | LABEL_SENSITIVE_CACHES)
