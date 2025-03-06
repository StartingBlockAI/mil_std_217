# repository.py

"""
Module: repository
Description: Contains the PartsRepository class for managing electronic parts.
"""

class PartsRepository:
    """
    Repository for managing electronic parts.
    
    Attributes:
        _parts (dict): Dictionary storing parts with part_number as keys.
    """
    def __init__(self):
        """Initializes the repository with an empty dictionary."""
        self._parts = {}

    def add_part(self, part):
        """
        Adds a part to the repository.
        
        Args:
            part (Part): An instance of a part (e.g., Resistor, Capacitor).
        """
        self._parts[part.part_number] = part

    def get_part(self, part_number):
        """
        Retrieves a part from the repository by its part number.
        
        Args:
            part_number (str): The unique identifier of the part.
        
        Returns:
            Part: The part instance if found, else None.
        """
        return self._parts.get(part_number)

    def list_parts(self):
        """
        Lists all part numbers in the repository.
        
        Returns:
            list: A list of part numbers.
        """
        return list(self._parts.keys())

