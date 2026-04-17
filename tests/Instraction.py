#!/usr/bin/env python3
"""
README.md Viewer - A complete PyQt6 application to read and display README files
Light Theme Version
"""

import sys
import os
import re
import html
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QFileDialog, QMessageBox, QLabel,
    QStatusBar, QSplitter, QTreeWidget, QTreeWidgetItem, QProgressBar,
    QToolBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize
from PyQt6.QtGui import QFont, QTextCursor, QAction, QIcon, QKeySequence, QFontMetrics


class MarkdownToHtmlConverter:
    """Convert Markdown to HTML with GitHub-like styling - Light Theme"""
    
    def __init__(self):
        self.code_blocks = []
    
    def convert(self, markdown_text):
        """Convert markdown to complete HTML document"""
        if not markdown_text:
            return self._get_empty_html()
        
        self.code_blocks = []
        html_content = markdown_text
        
        # Process in order
        html_content = self._extract_code_blocks(html_content)
        html_content = self._convert_headers(html_content)
        html_content = self._convert_emphasis(html_content)
        html_content = self._convert_lists(html_content)
        html_content = self._convert_links(html_content)
        html_content = self._convert_images(html_content)
        html_content = self._convert_blockquotes(html_content)
        html_content = self._convert_horizontal_rules(html_content)
        html_content = self._convert_tables(html_content)
        html_content = self._restore_code_blocks(html_content)
        html_content = self._convert_paragraphs(html_content)
        
        return self._wrap_html(html_content)
    
    def _extract_code_blocks(self, text):
        """Extract and store code blocks"""
        pattern = r'```(\w*)\n(.*?)```'
        
        def replace(match):
            lang = match.group(1) or 'text'
            code = match.group(2).strip()
            placeholder = f'__CODE_BLOCK_{len(self.code_blocks)}__'
            self.code_blocks.append({
                'lang': lang,
                'code': code,
                'placeholder': placeholder
            })
            return placeholder
        
        return re.sub(pattern, replace, text, flags=re.DOTALL)
    
    def _convert_headers(self, text):
        """Convert markdown headers to HTML"""
        # ATX style headers (# Header)
        def header_replacer(match):
            level = len(match.group(1))
            content = match.group(2).strip()
            return f'<h{level}>{content}</h{level}>'
        
        text = re.sub(r'^(#{1,6})\s+(.+?)\s*$', header_replacer, text, flags=re.MULTILINE)
        
        # Setext style headers (Header\n=== or ---)
        def setext_h1(match):
            return f'<h1>{match.group(1).strip()}</h1>'
        
        def setext_h2(match):
            return f'<h2>{match.group(1).strip()}</h2>'
        
        text = re.sub(r'^(.+?)\n=+$', setext_h1, text, flags=re.MULTILINE)
        text = re.sub(r'^(.+?)\n-+$', setext_h2, text, flags=re.MULTILINE)
        
        return text
    
    def _convert_emphasis(self, text):
        """Convert emphasis markers"""
        # Bold
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)
        
        # Italic
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        text = re.sub(r'_(.+?)_', r'<em>\1</em>', text)
        
        # Strikethrough
        text = re.sub(r'~~(.+?)~~', r'<del>\1</del>', text)
        
        # Inline code
        text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
        
        return text
    
    def _convert_lists(self, text):
        """Convert lists to HTML"""
        lines = text.split('\n')
        result = []
        in_ul = False
        in_ol = False
        in_task = False
        
        for line in lines:
            # Task list
            task_match = re.match(r'^[\*\-]\s+\[([ x])\]\s+(.+)$', line.strip())
            if task_match:
                if not in_task:
                    if in_ul:
                        result.append('</ul>')
                        in_ul = False
                    if in_ol:
                        result.append('</ol>')
                        in_ol = False
                    result.append('<ul class="task-list">')
                    in_task = True
                    in_ul = True
                
                checked = 'checked' if task_match.group(1) == 'x' else ''
                result.append(f'<li class="task-list-item"><input type="checkbox" {checked} disabled> {task_match.group(2)}</li>')
                continue
            
            # Unordered list
            ul_match = re.match(r'^[\*\-]\s+(.+)$', line.strip())
            if ul_match and not task_match:
                if not in_ul:
                    if in_ol:
                        result.append('</ol>')
                        in_ol = False
                    if in_task:
                        result.append('</ul>')
                        in_task = False
                    result.append('<ul>')
                    in_ul = True
                result.append(f'<li>{ul_match.group(1)}</li>')
                continue
            
            # Ordered list
            ol_match = re.match(r'^\d+\.\s+(.+)$', line.strip())
            if ol_match:
                if not in_ol:
                    if in_ul:
                        result.append('</ul>')
                        in_ul = False
                    if in_task:
                        result.append('</ul>')
                        in_task = False
                    result.append('<ol>')
                    in_ol = True
                result.append(f'<li>{ol_match.group(1)}</li>')
                continue
            
            # Close lists
            if in_ul:
                result.append('</ul>')
                in_ul = False
                in_task = False
            if in_ol:
                result.append('</ol>')
                in_ol = False
            result.append(line)
        
        # Close any remaining lists
        if in_ul:
            result.append('</ul>')
        if in_ol:
            result.append('</ol>')
        
        return '\n'.join(result)
    
    def _convert_links(self, text):
        """Convert markdown links to HTML"""
        # Inline links [text](url)
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
        
        # Reference links [text][ref] and [ref]:
        ref_links = re.findall(r'\[([^\]]+)\]\[([^\]]+)\]', text)
        for text_ref, ref_id in ref_links:
            text = text.replace(f'[{text_ref}][{ref_id}]', f'<a href="#{ref_id}">{text_ref}</a>')
        
        # Auto links <http://example.com>
        text = re.sub(r'<((https?://|mailto:)[^>]+)>', r'<a href="\1">\1</a>', text)
        
        return text
    
    def _convert_images(self, text):
        """Convert markdown images to HTML"""
        return re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1" style="max-width:100%;">', text)
    
    def _convert_blockquotes(self, text):
        """Convert blockquotes to HTML"""
        lines = text.split('\n')
        result = []
        in_blockquote = False
        blockquote_lines = []
        
        for line in lines:
            if line.startswith('> '):
                if not in_blockquote:
                    in_blockquote = True
                blockquote_lines.append(line[2:])
            else:
                if in_blockquote:
                    result.append(f'<blockquote>\n{"<br>".join(blockquote_lines)}\n</blockquote>')
                    blockquote_lines = []
                    in_blockquote = False
                result.append(line)
        
        if in_blockquote:
            result.append(f'<blockquote>\n{"<br>".join(blockquote_lines)}\n</blockquote>')
        
        return '\n'.join(result)
    
    def _convert_horizontal_rules(self, text):
        """Convert horizontal rules"""
        return re.sub(r'^([-\*_]){3,}$', '<hr>', text, flags=re.MULTILINE)
    
    def _convert_tables(self, text):
        """Convert markdown tables to HTML"""
        lines = text.split('\n')
        result = []
        i = 0
        
        while i < len(lines):
            # Look for table pattern
            if '|' in lines[i] and i + 1 < len(lines) and re.match(r'^[\|\s\-:]+$', lines[i + 1]):
                # Parse table
                headers = [cell.strip() for cell in lines[i].split('|')[1:-1]]
                alignments = []
                align_row = lines[i + 1].split('|')[1:-1]
                
                for cell in align_row:
                    if cell.strip().startswith(':') and cell.strip().endswith(':'):
                        alignments.append('center')
                    elif cell.strip().endswith(':'):
                        alignments.append('right')
                    else:
                        alignments.append('left')
                
                rows = []
                j = i + 2
                while j < len(lines) and '|' in lines[j]:
                    cells = [cell.strip() for cell in lines[j].split('|')[1:-1]]
                    rows.append(cells)
                    j += 1
                
                # Build HTML table
                table_html = '<table>\n<thead>\n<tr>\n'
                for idx, header in enumerate(headers):
                    align = alignments[idx] if idx < len(alignments) else 'left'
                    table_html += f'<th align="{align}">{header}</th>\n'
                table_html += '</tr>\n</thead>\n<tbody>\n'
                
                for row in rows:
                    table_html += '<tr>\n'
                    for idx, cell in enumerate(row):
                        align = alignments[idx] if idx < len(alignments) else 'left'
                        table_html += f'<td align="{align}">{cell}</td>\n'
                    table_html += '</tr>\n'
                
                table_html += '</tbody>\n</table>'
                result.append(table_html)
                i = j
            else:
                result.append(lines[i])
                i += 1
        
        return '\n'.join(result)
    
    def _restore_code_blocks(self, html):
        """Restore extracted code blocks"""
        for block in self.code_blocks:
            code_html = f'''<pre><code class="language-{block['lang']}">{html.escape(block['code'])}</code></pre>'''
            html = html.replace(block['placeholder'], code_html)
        return html
    
    def _convert_paragraphs(self, text):
        """Wrap text in paragraphs"""
        lines = text.split('\n')
        result = []
        in_paragraph = False
        paragraph_lines = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('<'):
                if not in_paragraph:
                    in_paragraph = True
                paragraph_lines.append(line)
            else:
                if in_paragraph:
                    result.append(f'<p>{" ".join(paragraph_lines)}</p>')
                    paragraph_lines = []
                    in_paragraph = False
                if line:
                    result.append(line)
        
        if in_paragraph:
            result.append(f'<p>{" ".join(paragraph_lines)}</p>')
        
        return '\n'.join(result)
    
    def _wrap_html(self, content):
        """Wrap content in complete HTML document - Light Theme"""
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>README.md Viewer</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            font-size: 16px;
            line-height: 1.6;
            color: #24292e;
            background-color: #ffffff;
            padding: 2rem;
        }}
        
        .container {{
            max-width: 1012px;
            margin: 0 auto;
            padding: 2rem;
            background: white;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
            line-height: 1.25;
        }}
        
        h1 {{
            font-size: 2em;
            border-bottom: 1px solid #eaecef;
            padding-bottom: 0.3em;
        }}
        
        h2 {{
            font-size: 1.5em;
            border-bottom: 1px solid #eaecef;
            padding-bottom: 0.3em;
        }}
        
        h3 {{ font-size: 1.25em; }}
        h4 {{ font-size: 1em; }}
        
        p {{
            margin-bottom: 16px;
        }}
        
        a {{
            color: #0366d6;
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        code {{
            font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', monospace;
            font-size: 85%;
            background-color: #f6f8fa;
            padding: 0.2em 0.4em;
            border-radius: 3px;
            color: #e83e8c;
        }}
        
        pre {{
            background-color: #f6f8fa;
            border-radius: 6px;
            padding: 16px;
            overflow: auto;
            line-height: 1.45;
            margin-bottom: 16px;
        }}
        
        pre code {{
            background-color: transparent;
            padding: 0;
            font-size: 100%;
            color: #24292e;
        }}
        
        blockquote {{
            padding: 0 1em;
            color: #6a737d;
            border-left: 0.25em solid #dfe2e5;
            margin: 0 0 16px 0;
        }}
        
        ul, ol {{
            padding-left: 2em;
            margin-bottom: 16px;
        }}
        
        li {{
            margin-bottom: 0.25em;
        }}
        
        hr {{
            height: 0.25em;
            padding: 0;
            margin: 24px 0;
            background-color: #e1e4e8;
            border: 0;
        }}
        
        img {{
            max-width: 100%;
            box-sizing: content-box;
            background-color: #fff;
        }}
        
        table {{
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 16px;
        }}
        
        th, td {{
            padding: 6px 13px;
            border: 1px solid #dfe2e5;
        }}
        
        th {{
            font-weight: 600;
            background-color: #f6f8fa;
        }}
        
        .task-list {{
            list-style: none;
            padding-left: 0;
        }}
        
        .task-list-item {{
            list-style: none;
            margin-bottom: 0.25em;
        }}
        
        .task-list-item input {{
            margin-right: 0.5em;
        }}
        
        @media (max-width: 768px) {{
            body {{
                padding: 1rem;
            }}
            .container {{
                padding: 1rem;
            }}
            table {{
                display: block;
                overflow-x: auto;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        {content}
    </div>
</body>
</html>'''
    
    def _get_empty_html(self):
        """Return HTML for empty content"""
        return self._wrap_html("<p><em>No content to display. Please open a README.md file.</em></p>")


class ReadmeLoader(QThread):
    """Thread for loading README files without blocking UI"""
    
    loaded = pyqtSignal(str, str)  # content, file_path
    error = pyqtSignal(str)
    
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
    
    def run(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.loaded.emit(content, self.file_path)
        except UnicodeDecodeError:
            try:
                with open(self.file_path, 'r', encoding='latin-1') as f:
                    content = f.read()
                self.loaded.emit(content, self.file_path)
            except Exception as e:
                self.error.emit(f"Failed to read file: {str(e)}")
        except Exception as e:
            self.error.emit(f"Failed to load file: {str(e)}")


class ReadmeViewer(QMainWindow):
    """Main application window for viewing README.md files"""
    
    def __init__(self):
        super().__init__()
        self.converter = MarkdownToHtmlConverter()
        self.current_file = None
        self.loader = None
        self.init_ui()
        self.setup_menu()
        self.check_for_readme()
    
    def init_ui(self):
        self.setWindowTitle("README.md Viewer - Light Theme")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set light theme style for the application
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f6f8fa;
            }
            QWidget {
                background-color: #f6f8fa;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create toolbar using QToolBar (proper way)
        self.create_toolbar()
        
        # Splitter for navigation and content
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Navigation sidebar
        self.nav_tree = QTreeWidget()
        self.nav_tree.setHeaderLabel("Table of Contents")
        self.nav_tree.itemClicked.connect(self.navigate_to_heading)
        self.nav_tree.setMaximumWidth(300)
        self.nav_tree.setStyleSheet("""
            QTreeWidget {
                background-color: #ffffff;
                border: 1px solid #e1e4e8;
                border-radius: 6px;
                font-size: 13px;
                margin: 5px;
            }
            QTreeWidget::item {
                padding: 4px;
            }
            QTreeWidget::item:hover {
                background-color: #f6f8fa;
            }
            QTreeWidget::item:selected {
                background-color: #0366d6;
                color: white;
            }
        """)
        splitter.addWidget(self.nav_tree)
        
        # Content area
        self.content_view = QTextEdit()
        self.content_view.setReadOnly(True)
        self.content_view.setStyleSheet("""
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #e1e4e8;
                border-radius: 6px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
                font-size: 14px;
                line-height: 1.6;
                margin: 5px;
                padding: 10px;
            }
        """)
        splitter.addWidget(self.content_view)
        
        # Set splitter proportions
        splitter.setSizes([250, 750])
        layout.addWidget(splitter)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #ffffff;
                border-top: 1px solid #e1e4e8;
                color: #586069;
            }
        """)
        self.status_bar.showMessage("Ready")
        
        # Progress bar (hidden by default)
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(200)
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)
    
    def create_toolbar(self):
        """Create the main toolbar"""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #ffffff;
                border: none;
                border-bottom: 1px solid #e1e4e8;
                spacing: 5px;
                padding: 5px;
            }
            QToolButton {
                background-color: #f6f8fa;
                border: 1px solid #e1e4e8;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 12px;
            }
            QToolButton:hover {
                background-color: #e1e4e8;
            }
            QToolButton:pressed {
                background-color: #d0d0d0;
            }
        """)
        
        # Add actions
        open_action = QAction("📂 Open README", self)
        open_action.triggered.connect(self.open_file)
        open_action.setToolTip("Open a README.md file")
        toolbar.addAction(open_action)
        
        reload_action = QAction("🔄 Reload", self)
        reload_action.triggered.connect(self.reload_file)
        reload_action.setToolTip("Reload current file")
        reload_action.setEnabled(False)
        toolbar.addAction(reload_action)
        
        export_action = QAction("💾 Export HTML", self)
        export_action.triggered.connect(self.export_html)
        export_action.setToolTip("Export as HTML file")
        export_action.setEnabled(False)
        toolbar.addAction(export_action)
        
        toolbar.addSeparator()
        
        toc_action = QAction("📑 Toggle TOC", self)
        toc_action.setCheckable(True)
        toc_action.setChecked(True)
        toc_action.triggered.connect(self.toggle_toc)
        toc_action.setToolTip("Show/Hide Table of Contents")
        toolbar.addAction(toc_action)
        
        toolbar.addSeparator()
        
        # Zoom actions
        zoom_out_action = QAction("🔍-", self)
        zoom_out_action.triggered.connect(self.zoom_out)
        zoom_out_action.setToolTip("Zoom out")
        toolbar.addAction(zoom_out_action)
        
        zoom_in_action = QAction("🔍+", self)
        zoom_in_action.triggered.connect(self.zoom_in)
        zoom_in_action.setToolTip("Zoom in")
        toolbar.addAction(zoom_in_action)
        
        reset_zoom_action = QAction("100%", self)
        reset_zoom_action.triggered.connect(self.reset_zoom)
        reset_zoom_action.setToolTip("Reset zoom")
        toolbar.addAction(reset_zoom_action)
        
        toolbar.addSeparator()
        
        # File info label widget
        self.file_label = QLabel("No file loaded")
        self.file_label.setStyleSheet("color: #586069; font-size: 11px; padding: 0 10px;")
        
        # Create a widget to hold the label and add it to toolbar
        label_widget = QWidget()
        label_layout = QHBoxLayout(label_widget)
        label_layout.setContentsMargins(0, 0, 0, 0)
        label_layout.addWidget(self.file_label)
        toolbar.addWidget(label_widget)
        
        self.addToolBar(toolbar)
        
        # Store references for enabling/disabling
        self.reload_action = reload_action
        self.export_action = export_action
    
    def setup_menu(self):
        """Setup menu bar"""
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #ffffff;
                border-bottom: 1px solid #e1e4e8;
            }
            QMenuBar::item:selected {
                background-color: #f6f8fa;
            }
            QMenu {
                background-color: #ffffff;
                border: 1px solid #e1e4e8;
            }
            QMenu::item:selected {
                background-color: #0366d6;
                color: white;
            }
        """)
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        open_action = QAction("&Open README...", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        reload_action = QAction("&Reload", self)
        reload_action.setShortcut(QKeySequence.StandardKey.Refresh)
        reload_action.triggered.connect(self.reload_file)
        file_menu.addAction(reload_action)
        
        file_menu.addSeparator()
        
        export_action = QAction("&Export as HTML...", self)
        export_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        export_action.triggered.connect(self.export_html)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        toggle_toc_action = QAction("Toggle Table of Contents", self)
        toggle_toc_action.setShortcut("Ctrl+T")
        toggle_toc_action.triggered.connect(self.toggle_toc)
        view_menu.addAction(toggle_toc_action)
        
        view_menu.addSeparator()
        
        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.setShortcut(QKeySequence.StandardKey.ZoomIn)
        zoom_in_action.triggered.connect(self.zoom_in)
        view_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.setShortcut(QKeySequence.StandardKey.ZoomOut)
        zoom_out_action.triggered.connect(self.zoom_out)
        view_menu.addAction(zoom_out_action)
        
        reset_zoom_action = QAction("Reset Zoom", self)
        reset_zoom_action.setShortcut("Ctrl+0")
        reset_zoom_action.triggered.connect(self.reset_zoom)
        view_menu.addAction(reset_zoom_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def check_for_readme(self):
        """Check if README.md exists in current directory"""
        readme_paths = ["README.md", "readme.md", "Readme.md", "README.MD"]
        
        for path in readme_paths:
            if os.path.exists(path):
                self.load_file(path)
                break
    
    def open_file(self):
        """Open file dialog to select README.md"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open README.md",
            "",
            "Markdown Files (README.md *.md);;All Files (*)"
        )
        
        if file_path:
            self.load_file(file_path)
    
    def load_file(self, file_path):
        """Load and display a markdown file"""
        # Show progress
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate
        self.status_bar.showMessage(f"Loading {os.path.basename(file_path)}...")
        
        # Start loader thread
        self.loader = ReadmeLoader(file_path)
        self.loader.loaded.connect(self.on_file_loaded)
        self.loader.error.connect(self.on_load_error)
        self.loader.start()
    
    def on_file_loaded(self, content, file_path):
        """Handle successful file load"""
        self.current_file = file_path
        self.file_label.setText(f"📄 {os.path.basename(file_path)}")
        
        # Enable actions
        self.reload_action.setEnabled(True)
        self.export_action.setEnabled(True)
        
        # Convert and display
        html = self.converter.convert(content)
        self.content_view.setHtml(html)
        
        # Build table of contents
        self.build_table_of_contents(content)
        
        # Hide progress
        self.progress_bar.setVisible(False)
        self.status_bar.showMessage(f"Loaded: {os.path.basename(file_path)}", 3000)
    
    def on_load_error(self, error_msg):
        """Handle file load error"""
        self.progress_bar.setVisible(False)
        self.status_bar.showMessage("Error loading file", 3000)
        QMessageBox.critical(self, "Error", error_msg)
    
    def reload_file(self):
        """Reload the current file"""
        if self.current_file and os.path.exists(self.current_file):
            self.load_file(self.current_file)
        else:
            QMessageBox.warning(self, "Warning", "File no longer exists!")
            self.reload_action.setEnabled(False)
    
    def build_table_of_contents(self, markdown_content):
        """Build table of contents from headers"""
        self.nav_tree.clear()
        
        # Find all headers
        header_pattern = r'^(#{1,6})\s+(.+)$'
        headers = []
        
        for line in markdown_content.split('\n'):
            match = re.match(header_pattern, line.strip())
            if match:
                level = len(match.group(1))
                title = match.group(2).strip()
                headers.append((level, title))
        
        if not headers:
            item = QTreeWidgetItem(["No headers found"])
            self.nav_tree.addTopLevelItem(item)
            return
        
        # Build tree structure
        root_items = {}
        
        for level, title in headers:
            item = QTreeWidgetItem([title])
            item.setData(0, Qt.ItemDataRole.UserRole, title)
            
            # Find parent
            parent = None
            for lvl in range(level - 1, 0, -1):
                if lvl in root_items and root_items[lvl]:
                    parent = root_items[lvl][-1]
                    break
            
            if parent:
                parent.addChild(item)
            else:
                self.nav_tree.addTopLevelItem(item)
            
            # Store in stack
            for lvl in range(level, 7):
                if lvl not in root_items:
                    root_items[lvl] = []
                if lvl == level:
                    root_items[lvl].append(item)
                else:
                    root_items[lvl] = []
        
        # Expand all items
        self.nav_tree.expandAll()
    
    def navigate_to_heading(self, item, column):
        """Navigate to selected heading"""
        heading = item.data(0, Qt.ItemDataRole.UserRole)
        if heading:
            # Search for heading in content
            content_text = self.content_view.toPlainText()
            pos = content_text.find(heading)
            if pos != -1:
                cursor = self.content_view.textCursor()
                cursor.setPosition(pos)
                self.content_view.setTextCursor(cursor)
                self.content_view.ensureCursorVisible()
    
    def toggle_toc(self, checked):
        """Show/hide table of contents"""
        self.nav_tree.setVisible(checked)
    
    def zoom_in(self):
        """Increase font size"""
        current_font = self.content_view.font()
        current_size = current_font.pointSize()
        if current_size < 24:
            current_font.setPointSize(current_size + 1)
            self.content_view.setFont(current_font)
            self.status_bar.showMessage(f"Zoom: {current_size + 1}pt", 1000)
    
    def zoom_out(self):
        """Decrease font size"""
        current_font = self.content_view.font()
        current_size = current_font.pointSize()
        if current_size > 8:
            current_font.setPointSize(current_size - 1)
            self.content_view.setFont(current_font)
            self.status_bar.showMessage(f"Zoom: {current_size - 1}pt", 1000)
    
    def reset_zoom(self):
        """Reset font size to default"""
        font = QFont()
        font.setPointSize(10)
        self.content_view.setFont(font)
        self.status_bar.showMessage("Zoom reset to 100%", 1000)
    
    def export_html(self):
        """Export current view as HTML file"""
        if not self.current_file:
            QMessageBox.warning(self, "Warning", "No file loaded to export!")
            return
        
        default_name = os.path.splitext(self.current_file)[0] + ".html"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export as HTML",
            default_name,
            "HTML Files (*.html);;All Files (*)"
        )
        
        if file_path:
            try:
                # Get current HTML content
                html_content = self.content_view.toHtml()
                
                # Write to file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                self.status_bar.showMessage(f"Exported to {os.path.basename(file_path)}", 3000)
                QMessageBox.information(self, "Success", f"HTML exported successfully to:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export: {str(e)}")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
        <h2>README.md Viewer</h2>
        <p>A complete application to view and read README.md files.</p>
        <h3>Features:</h3>
        <ul>
            <li>Full Markdown support</li>
            <li>Table of contents navigation</li>
            <li>Clean light theme design</li>
            <li>Export to HTML</li>
            <li>Zoom controls</li>
            <li>Keyboard shortcuts</li>
        </ul>
        <p>Built with PyQt6</p>
        <p>Version 1.0.0</p>
        """
        QMessageBox.about(self, "About README.md Viewer", about_text)


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Set application metadata
    app.setApplicationName("README.md Viewer")
    app.setApplicationVersion("1.0.0")
    
    # Create and show main window
    window = ReadmeViewer()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()