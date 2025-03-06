# mil_std_217

Objective:
Develop a repository to look up reliability values for electronic parts as defined by MIL-HDBK-217)

Key Data Points:
For each part, define what attributes are required such as part number, base failure rate, quality factor, environmental factor, and possibly additional attributes specific to the type of component. (e.g. resistance value for resistors, capacitance for capacitors).

Functionality:
Extensibly look up calculated failure rates, store different types of parts, and enable lookups by part number or type.

##Project Architecture
Base Class (Part): Holds common attributes and methods (e.g. failure rate calculation).

Subclasses (e.g. Resistor, Capacitor): Inherit from Part and include additional, type-specific attributes.

##Repository Pattern:
PartsRepository that will manage part objects (adding, retrieving, listing)

##Project Structure:
Code is split into modules to improve maintainability and scalability

project/
│
├── parts.py         # Contains the Part base class and its subclasses
├── repository.py    # Contains the PartsRepository class
├── main.py          # The main file that ties everything together
├── requirements.txt # List of required packages (if any)
├── README.md        # Instructions on setting up and running the project
└── .gitignore       # To ignore the virtual environment folder and other artifacts

Virtual Environment:
python -m venv 217venv
add 217venv to .gitignore
from cmd: .\217venv\Scripts\activate

To create new requirements.txt file:
pip freeze > requirements

To create new requirements.txt file only using utilized packages:
pipreqs /path/to/your/project

To overwrite an existing file:
pipreqs . --force

