from abc import abstractmethod, ABC

class TodoistObject(ABC):
    """
    Generic class for objects which have an ID and a dataclass from the API.
    __new__ is overridden to return the same instance for a given ID.
    """
    __registry = {}

    def __new__(cls, _id, env):
        # This ensures that only one instance of each object exists for a given ID
        key = (cls, _id, env)
        if key in cls.__registry:
            return cls.__registry[key]
        else:
            instance = super(TodoistObject, cls).__new__(cls)
            cls.__registry[key] = instance
            return instance

    def __init__(self, _id, env):
        self._id = _id
        self.env = env

    @abstractmethod
    def _data(self):
        raise NotImplementedError("Subclasses should implement this property")

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self._id}>"
