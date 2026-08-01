import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView

class SchoolHTMLViewer(QMainWindow):
    def __init__(self, html_path=None):
        super().__init__()
        self.setWindowTitle("Guintas Elementary School")
        self.setMinimumSize(900, 700)
        
        # Setup UI
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        central_widget.setLayout(layout)
        
        # Web view
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)
        
        # Load HTML
        if html_path:
            self.load_html_file(html_path)
        else:
            self.load_default_html()
    
    def load_html_file(self, html_path):
        """Load HTML from a file path"""
        if os.path.exists(html_path):
            abs_path = os.path.abspath(html_path)
            self.web_view.load(QUrl.fromLocalFile(abs_path))
            self.setWindowTitle(f"Guintas Elementary School - {os.path.basename(html_path)}")
        else:
            print(f"Error: File not found: {html_path}")
            self.load_default_html()
    
    def load_html_content(self, html_string):
        """Load HTML from a string"""
        self.web_view.setHtml(html_string)
    
    def load_default_html(self):
        """Load default HTML content"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Guintas Elementary School</title>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
            <style>
                body {
                    font-family: 'Segoe UI', Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    margin: 0;
                    background: linear-gradient(145deg, #f6f9fc, #e6f0f5);
                }
                .card {
                    background: white;
                    padding: 50px;
                    border-radius: 30px;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.15);
                    text-align: center;
                    max-width: 700px;
                }
                h1 {
                    color: #1b4e3f;
                    font-size: 3em;
                    margin: 20px 0 10px;
                }
                .location {
                    color: #2b7a62;
                    font-size: 1.5em;
                    border-top: 2px dashed #d7e6e0;
                    padding-top: 20px;
                    margin-top: 10px;
                }
                .info {
                    margin-top: 30px;
                    display: flex;
                    gap: 20px;
                    justify-content: center;
                    flex-wrap: wrap;
                }
                .badge {
                    background: #f2faf7;
                    padding: 10px 20px;
                    border-radius: 30px;
                    border: 1px solid #2b7a62;
                }
            </style>
        </head>
        <body>
            <div class="card">
                <i class="fas fa-school" style="font-size: 3em; color: #2b7a62;"></i>
                <h1>Guintas Elementary School</h1>
                <div class="location">
                    <i class="fas fa-map-pin"></i> Guintas, Leganes, Iloilo
                </div>
                <div class="info">
                    <span class="badge"><i class="fas fa-flag"></i> Region VI</span>
                    <span class="badge"><i class="fas fa-calendar"></i> Est. 1968</span>
                    <span class="badge"><i class="fas fa-users"></i> ~340 students</span>
                </div>
            </div>
        </body>
        </html>
        """
        self.web_view.setHtml(html_content)

def main():
    app = QApplication(sys.argv)
    
    # Specify your HTML file path
    html_path = r"C:\Users\O.Feronel\OneDrive - ams OSRAM\Documents\PYTHON_EXTERN_PROJ\GUINTAS_ELEM_GRADING_SYSTEM\html\Header.html"
    
    # Create viewer with HTML file
    viewer = SchoolHTMLViewer(html_path)
    viewer.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()