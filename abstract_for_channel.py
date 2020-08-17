from abc import ABC, abstractmethod


class AbstractCannel(ABC):
    """ """

    @abstractmethod
    def write_uzer_db(self):
        """Writes the number of users to the database."""
        pass
