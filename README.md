
## Features:

1. **Complete Markdown Support**:
   - Headers (## Header)
   - Bold/Italic/Strikethrough
   - Code blocks with syntax highlighting
   - Lists (ordered/unordered)
   - Links and images
   - Blockquotes
   - Horizontal rules

2. **Live Preview**: Real-time HTML preview while typing

3. **File Operations**: Open, save, save as markdown files

4. **Export to HTML**: Export rendered markdown as standalone HTML

5. **Syntax Highlighting**: Visual highlighting for markdown syntax in editor

6. **Clean UI**: Split-pane interface with toolbar

7. **Dark/Light Mode**: Adapts to system theme

## Usage:

```python
# Simple usage
editor = MarkdownEditor()
editor.set_markdown("# Hello World")
html_output = editor.get_html()

# Viewer only
viewer = MarkdownViewer()
viewer.load_file("document.md")

# Convert programmatically
converter = MarkdownConverter()
html = converter.convert(markdown_text)