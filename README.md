# GES Grading System

A full-featured elementary grading system built with **PyQt6** and **SQLite**. This application is designed for primary school workflows that need student management, academic master data, grading inputs, and adviser dashboards in a modern desktop UI.

## What This Project Offers

- Complete student lifecycle management
- Grade level and section management
- Subject and adviser assignment functionality
- Grade entry, monitoring, and report-ready data handling
- SQLite persistence with CRUD operations for all academic entities
- Custom UI components and animated workflows
- Screen-aware application placement for multi-monitor setups
- Modular layout and form architecture for extensibility

## Key Features

- **Student Management**: create, update, and manage students, guardians, and assigned sections
- **Grade Levels**: maintain grade-level master data from Kinder through Grade 6
- **Subject Management**: define subjects, assign subject teachers, and track academic offerings
- **Grading Module**: collect grading data with support for custom subject grading inputs
- **Adviser Interface**: adviser-specific dashboards and workflows
- **Authentication**: login workflow is implemented and ready for enhancement
- **Responsive UI**: dynamic forms, animated page transitions, custom tables, and notification flows
- **Sample Data Support**: includes sample academic records for fast verification and testing

## Technology Stack

- Python 3.8+
- PyQt6
- SQLite (built into Python)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/OliverFeronel090597/GES_Grading_App.git
cd GUINTAS_ELEM_GRADING_SYSTEM
```

2. Create and activate a virtual environment (recommended):

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python src/main.py
```

## Project Layout

- `src/main.py` — application entry point and main event loop
- `src/MainWindow.py` — primary window class and navigation container
- `src/Adviser/` — adviser-specific modules and workflow components
- `src/forms/` — reusable form components and dialog screens
- `src/layouts/` — page layouts, custom widgets, and UI helpers
- `src/utils/` — utility modules used across the application
- `src/img/` — image assets used by the user interface

## Application Flow

1. `main.py` initializes `QApplication`, installs a global activity logger, and loads `GES_StudentGrading`
2. `MainWindow.py` manages the main UI state and navigation
3. Layout modules under `src/layouts` implement individual screens such as:
   - login page
   - home dashboard
   - student registry
   - grade level management
   - subject management
   - grade entry workflows
4. The app uses an SQLite database backend and supports full CRUD for academic entities

## Development Notes

- `src/main.py` includes a helper to move the window to a second display when available
- `layouts/Globalenentfilter.py` provides global event logging for user interactions
- Several commented sections in `main.py` are intentionally left for future logging/debug support
- The login system is present and can be extended with hashing, role privileges, or external authentication

## Running Tests

There is a `tests/` folder containing sample test modules and database experiments. To run tests, use a supported test runner after reviewing the test files.

Example:

```bash
python -m pytest tests
```

> Note: The repository appears to include exploratory and backup files under `tests/`. Review them before use.

## Improving the App

Suggested next enhancements:

- Add database migration/versioning support
- Implement role-based security and password hashing
- Add export reports to PDF or Excel
- Build a print-ready grade summary screen
- Add a real settings/manage configuration module
- Convert layout components to `.ui` forms or QML for easier design updates

## Contributing

1. Fork the repository
2. Create a branch with a clear name: `feature/<description>` or `fix/<description>`
3. Add or update tests for new functionality
4. Run the application and verify changes
5. Submit a pull request with a summary of changes

## License

This project is provided under the MIT License. See `LICENSE` for full details.

---

## Contact

For questions, improvements, or bug reports, please open an issue or connect with the project maintainer through the repository.
"# GES_Grading_App" 
