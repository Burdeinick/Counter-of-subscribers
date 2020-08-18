from abc import ABC, abstractmethod


class AbstractCannel(ABC):
    """ """
    @abstractmethod
    def pars_url(self, url: str) -> str:
        """ """
        pass 

    @abstractmethod
    def get_size_group(self):
        """ """
        pass

    @abstractmethod
    def picking_info(self):
        """Writes the number of users to the database."""
        pass

