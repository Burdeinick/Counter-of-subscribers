from abc import ABC, abstractmethod


class AbstractCannel(ABC):
    """All inheritors of this class must have all its methods."""
    @abstractmethod
    def get_size_group(self):
        """This method must fixate number of community members."""
        pass

    @abstractmethod
    def picking_info(self) -> tuple:
        """This method should return a tuple that
        contains the channel id in the DB and the number
        of subscribers of the group.

        """
        pass
