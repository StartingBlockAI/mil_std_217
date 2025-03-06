"""
Module: parts
Description: Contains the base Part class and its subclasses for representing electronic parts.
"""

class Part:
    """
    Base class for electronic parts.
    
    Attributes:
        part_number (str): Unique identifier for the part.
        base_failure_rate (float): The base failure rate for the part.
        quality_factor (float): Factor representing part quality.
        environmental_factor (float): Factor representing environmental impact on reliability.
    """
    def __init__(self, part_number, base_failure_rate, quality_factor, environmental_factor):
        """
        Initializes a Part instance.
        
        Args:
            part_number (str): Unique part identifier.
            base_failure_rate (float): Base failure rate.
            quality_factor (float): Quality factor.
            environmental_factor (float): Environmental factor.
        """
        self.part_number = part_number
        self.base_failure_rate = base_failure_rate
        self.quality_factor = quality_factor
        self.environmental_factor = environmental_factor

    def calculate_failure_rate(self):
        """
        Calculates the overall failure rate based on the base failure rate, quality factor, and environmental factor.
        
        Returns:
            float: The calculated failure rate.
        """
        return self.base_failure_rate * self.quality_factor * self.environmental_factor

    def __repr__(self):
        """
        Returns a string representation of the Part.
        
        Returns:
            str: String representation of the part.
        """
        return f"<Part {self.part_number}: Failure Rate = {self.calculate_failure_rate():.4f}>"

class Resistor(Part):
    """
    Represents a resistor component.
    
    Attributes:
        resistance_value (float): Resistance value in ohms.
    """
    def __init__(self, part_number, base_failure_rate, quality_factor, environmental_factor, resistance_value):
        """
        Initializes a Resistor instance.
        
        Args:
            part_number (str): Unique identifier.
            base_failure_rate (float): Base failure rate.
            quality_factor (float): Quality factor.
            environmental_factor (float): Environmental factor.
            resistance_value (float): Resistance value in ohms.
        """
        super().__init__(part_number, base_failure_rate, quality_factor, environmental_factor)
        self.resistance_value = resistance_value

class Capacitor(Part):
    """
    Represents a capacitor component.
    
    Attributes:
        capacitance_value (float): Capacitance value in farads.
    """
    def __init__(self, part_number, base_failure_rate, quality_factor, environmental_factor, capacitance_value):
        """
        Initializes a Capacitor instance.
        
        Args:
            part_number (str): Unique identifier.
            base_failure_rate (float): Base failure rate.
            quality_factor (float): Quality factor.
            environmental_factor (float): Environmental factor.
            capacitance_value (float): Capacitance value in farads.
        """
        super().__init__(part_number, base_failure_rate, quality_factor, environmental_factor)
        self.capacitance_value = capacitance_value

