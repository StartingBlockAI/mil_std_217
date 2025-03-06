"""
Module: main
Description: Main entry point for the reliability parts repository application.
"""

from parts import Resistor, Capacitor
from repository import PartsRepository

def main():
    """
    Main function to run the reliability parts repository application.
    
    It creates a repository, adds sample parts (resistor and capacitor), and displays details of a part.
    """
    # Initialize the repository
    repo = PartsRepository()

    # Create sample parts with hypothetical values
    resistor = Resistor("R-1001", base_failure_rate=0.002, quality_factor=1.1, environmental_factor=1.0, resistance_value=1000)
    capacitor = Capacitor("C-2001", base_failure_rate=0.001, quality_factor=1.2, environmental_factor=0.9, capacitance_value=1e-6)

    # Add parts to the repository
    repo.add_part(resistor)
    repo.add_part(capacitor)

    # Lookup a part and print its details
    part = repo.get_part("R-1001")
    print(part)

if __name__ == "__main__":
    main()
