from PyQt6.QtWidgets import (
    QTableWidget, QTableWidgetItem, QMenu
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QPoint


class SmartTable(QTableWidget):
    """
    A customizable and reusable QTableWidget with optional:
        - Context menu (Add / Edit / Delete)
        - Double-click callback
        - Row-only clearing
        - Automatic data + header loading
        - Optional search/filter by column or text

    Main Features:
        ✔ Alternating row colors
        ✔ Row selection only
        ✔ Non-editable cells
        ✔ Optional context menu
        ✔ Optional double-click callback
        ✔ Clear rows but keep headers
        ✔ Simple callbacks for Add/Edit/Delete/Double-click
        ✔ Search/filter rows dynamically

    Args:
        parent (QWidget | None):
            Optional parent widget.
        enable_context_menu (bool):
            If True, enables right-click context menu.
        enable_double_click (bool):
            If True, enables double-click signal callback.

    Callbacks:
        cb_add:         func()
        cb_edit:        func(row_index)
        cb_delete:      func(row_index)
        cb_double_click:func(row_index)

    Example:
        table = SmartTable(enable_context_menu=True, enable_double_click=True)
        table.set_actions(add=on_add, edit=on_edit, delete=on_delete)

        table.update_data(
            data=[[1, "Item A"], [2, "Item B"]],
            headers=["ID", "Name"]
        )

        # Filter by specific column
        table.search("Item", column="Name")

        # Filter by all columns
        table.search("1")

        table.clear_table()   # clears rows only
    """
    def __init__(
        self,
        parent=None,
        enable_context_menu=True,
        enable_double_click=True,
        enable_vertical_header=True,
        
    ):
        """Initialize SmartTable and configure UI behavior."""
        super().__init__(parent)

        # Initialize table structure
        self.setRowCount(0)
        self.setColumnCount(0)

        # UI defaults
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.horizontalHeader().setStretchLastSection(True)

        # Feature flags
        self._context_enabled = enable_context_menu
        self._double_click_enabled = enable_double_click

        # Context menu setup
        if enable_context_menu:
            self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            self.customContextMenuRequested.connect(self._open_menu)

        # Double-click callback
        self.cb_double_click = None
        if enable_double_click:
            self.itemDoubleClicked.connect(self._on_double_click)

        #Virtical Header
        self.verticalHeader().setVisible(enable_vertical_header)

        # Right-click menu callbacks
        self.cb_add = None
        self.cb_edit = None
        self.cb_delete = None

    # -------------------------------------------------------------
    # PUBLIC: Update data & headers
    # -------------------------------------------------------------
    def update_data(self, data: list[list], headers: list[str], filter_text: str = None, filter_column: str = "GradeLevel"):
        """
        Update the table with data and headers, optionally filtering rows by a specific column.

        Args:
            data (list[list]): The rows of data.
            headers (list[str]): Column headers.
            filter_text (str | None): Text to filter rows by.
            filter_column (str): Name of the column to apply the filter.
        """
        self.clear()
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)

        # Determine the index of the column to filter
        filter_idx = headers.index(filter_column) if filter_text and filter_column in headers else None

        # Filter rows
        if filter_text and filter_idx is not None:
            filter_text_lower = filter_text.lower()
            filtered_data = [
                row for row in data
                if filter_text_lower in str(row[filter_idx]).lower()
            ]
        else:
            filtered_data = data

        self.setRowCount(len(filtered_data))

        # Populate the table
        for r, row in enumerate(filtered_data):
            for c, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setItem(r, c, item)
    # -------------------------------------------------------------
    # PUBLIC: Assign menu + double-click callbacks
    # -------------------------------------------------------------
    def set_actions(self, add=None, edit=None, delete=None, double_click=None):
        """
        Assign user-defined callbacks for context menu and double-click.

        Args:
            add (callable | None):
                Callback when "Add" is clicked. Signature: func()

            edit (callable | None):
                Callback when "Edit" is clicked.
                Signature: func(row_index)

            delete (callable | None):
                Callback when "Delete" is clicked.
                Signature: func(row_index)

            double_click (callable | None):
                Callback when a row is double-clicked.
                Signature: func(row_index)

        Notes:
            - Any callback may be set to None.
            - If no row is selected, Edit/Delete are ignored.
        """
        self.cb_add = add
        self.cb_edit = edit
        self.cb_delete = delete
        self.cb_double_click = double_click

    # -------------------------------------------------------------
    # PUBLIC: Clear only rows
    # -------------------------------------------------------------
    def clear_table(self):
        """
        Clears only the row data but keeps headers and column count.

        Useful when refreshing data without rebuilding the table structure.

        Example:
            table.clear_table()
        """
        self.setRowCount(0)

    # -------------------------------------------------------------
    # INTERNAL: Open context menu
    # -------------------------------------------------------------
    def _open_menu(self, pos: QPoint):
        """
        Internal handler for right-click context menu.

        Args:
            pos (QPoint):
                Position within the widget where the menu was requested.

        Behavior:
            - Adds Add / Edit / Delete options.
            - Triggers the corresponding callback if defined.
        """
        if not self._context_enabled:
            return

        menu = QMenu(self)

        act_add = QAction("Add", self)
        act_edit = QAction("Edit", self)
        act_delete = QAction("Delete", self)

        menu.addAction(act_add)
        menu.addAction(act_edit)
        menu.addAction(act_delete)

        clicked = menu.exec(self.mapToGlobal(pos))
        row = self.currentRow()

        if clicked == act_add and self.cb_add:
            self.cb_add()

        elif clicked == act_edit and self.cb_edit and row >= 0:
            self.cb_edit(row)

        elif clicked == act_delete and self.cb_delete and row >= 0:
            self.cb_delete(row)

    # -------------------------------------------------------------
    # INTERNAL: Handle double-click event
    # -------------------------------------------------------------
    def _on_double_click(self, item):
        """
        Internal handler for item double-click.

        Args:
            item (QTableWidgetItem):
                The clicked item.

        Behavior:
            - Invokes cb_double_click(row_index) if enabled.
        """
        if not self._double_click_enabled:
            return

        if self.cb_double_click:
            self.cb_double_click(item.row())

    # -------------------------------------------------------------
    # PUBLIC: Search/filter table
    # -------------------------------------------------------------
    def search(self, text: str, column: str = None):
        """
        Filter the table rows by text.

        Args:
            text (str): Text to search for (case-insensitive).
            column (str | None): Column name to filter by. If None, searches all columns.
        """
        text_lower = text.lower()
        for r in range(self.rowCount()):
            match = False
            # If column is specified, find its index
            if column and column in [self.horizontalHeaderItem(c).text() for c in range(self.columnCount())]:
                c_idx = [self.horizontalHeaderItem(c).text() for c in range(self.columnCount())].index(column)
                item = self.item(r, c_idx)
                if item and text_lower in item.text().lower():
                    match = True
            else:
                # Search all columns
                for c in range(self.columnCount()):
                    item = self.item(r, c)
                    if item and text_lower in item.text().lower():
                        match = True
                        break

            # Show or hide the row
            self.setRowHidden(r, not match)