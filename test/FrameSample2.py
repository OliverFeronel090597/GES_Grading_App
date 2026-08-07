import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QFrame, QLabel, QScrollArea
)
from PyQt6.QtCore import Qt

class AllQSSPropertiesDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("All QFrame QSS Properties")
        self.setGeometry(100, 100, 800, 900)
        
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        
        # Scroll area to contain all examples
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: #f5f6fa; }")
        
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(20)
        
        # Example 1: Basic Frame with all common properties
        frame1 = QFrame()
        frame1.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 #3498db, stop:1 #2980b9);
                border: 3px solid #2c3e50;
                border-radius: 10px;
                padding: 20px;
                color: white;
                font-size: 16px;
                font-weight: bold;
                text-align: center;
                min-height: 80px;
            }
        """)
        label1 = QLabel("GRADIENT BACKGROUND WITH BORDER")
        label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label1.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        layout1 = QVBoxLayout(frame1)
        layout1.addWidget(label1)
        container_layout.addWidget(frame1)
        
        # Example 2: Box Shadow and Text Shadow
        frame2 = QFrame()
        frame2.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 2px solid #e74c3c;
                border-radius: 15px;
                padding: 20px;
                box-shadow: 5px 5px 15px rgba(231, 76, 60, 0.4),
                           inset 0 0 20px rgba(231, 76, 60, 0.1);
                font-size: 14px;
                color: #2c3e50;
                text-align: center;
                min-height: 80px;
                font-weight: bold;
            }
            QFrame:hover {
                box-shadow: 8px 8px 25px rgba(231, 76, 60, 0.6);
                transform: scale(1.02);
                transition: all 0.3s ease;
            }
        """)
        label2 = QLabel("BOX SHADOW & TEXT SHADOW")
        label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label2.setStyleSheet("""
            color: #2c3e50;
            font-size: 16px;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        """)
        layout2 = QVBoxLayout(frame2)
        layout2.addWidget(label2)
        container_layout.addWidget(frame2)
        
        # Example 3: Dotted Border with Custom Padding
        frame3 = QFrame()
        frame3.setStyleSheet("""
            QFrame {
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.5,
                                          stop:0 #f1c40f, stop:1 #f39c12);
                border: 4px dotted #e67e22;
                border-radius: 20px 5px 20px 5px;
                padding: 30px 20px 30px 20px;
                margin: 10px;
                color: #2c3e50;
                font-size: 14px;
                text-align: center;
                min-height: 80px;
                font-weight: bold;
                text-shadow: 1px 1px 2px rgba(255,255,255,0.5);
            }
        """)
        label3 = QLabel("DOTTED BORDER WITH RADIAL GRADIENT")
        label3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label3.setStyleSheet("color: #2c3e50; font-size: 16px; font-weight: bold;")
        layout3 = QVBoxLayout(frame3)
        layout3.addWidget(label3)
        container_layout.addWidget(frame3)
        
        # Example 4: Dashed Border with Animation
        frame4 = QFrame()
        frame4.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border: 3px dashed #ecf0f1;
                border-radius: 10px;
                padding: 20px;
                color: #ecf0f1;
                font-size: 16px;
                font-weight: bold;
                text-align: center;
                min-height: 80px;
                animation: pulse 2s infinite;
            }
            @keyframes pulse {
                0% { background-color: #2c3e50; border-color: #ecf0f1; }
                50% { background-color: #34495e; border-color: #3498db; }
                100% { background-color: #2c3e50; border-color: #ecf0f1; }
            }
        """)
        label4 = QLabel("ANIMATED DASHED BORDER")
        label4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label4.setStyleSheet("color: #ecf0f1; font-size: 16px; font-weight: bold;")
        layout4 = QVBoxLayout(frame4)
        layout4.addWidget(label4)
        container_layout.addWidget(frame4)
        
        # Example 5: Double Border with Multiple Shadows
        frame5 = QFrame()
        frame5.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #9b59b6, stop:1 #8e44ad);
                border: 5px double #ecf0f1;
                border-radius: 30px;
                padding: 20px;
                color: white;
                font-size: 16px;
                font-weight: bold;
                text-align: center;
                min-height: 80px;
                box-shadow: 0 10px 20px rgba(0,0,0,0.3),
                           inset 0 0 30px rgba(255,255,255,0.1);
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
        """)
        label5 = QLabel("DOUBLE BORDER WITH GRADIENT")
        label5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label5.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        layout5 = QVBoxLayout(frame5)
        layout5.addWidget(label5)
        container_layout.addWidget(frame5)
        
        # Example 6: Groove Border with Filter Effects
        frame6 = QFrame()
        frame6.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 #ecf0f1, stop:1 #bdc3c7);
                border: 6px groove #2c3e50;
                border-radius: 15px;
                padding: 20px;
                color: #2c3e50;
                font-size: 16px;
                font-weight: bold;
                text-align: center;
                min-height: 80px;
                filter: drop-shadow(5px 5px 10px rgba(0,0,0,0.3));
            }
        """)
        label6 = QLabel("GROOVE BORDER WITH DROP SHADOW")
        label6.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label6.setStyleSheet("color: #2c3e50; font-size: 16px; font-weight: bold;")
        layout6 = QVBoxLayout(frame6)
        layout6.addWidget(label6)
        container_layout.addWidget(frame6)
        
        # Example 7: Ridge Border with Transform
        frame7 = QFrame()
        frame7.setStyleSheet("""
            QFrame {
                background: qconicalgradient(cx:0.5, cy:0.5, angle:0,
                                           stop:0 #e74c3c, stop:0.25 #f1c40f,
                                           stop:0.5 #2ecc71, stop:0.75 #3498db,
                                           stop:1 #9b59b6);
                border: 6px ridge #2c3e50;
                border-radius: 20px;
                padding: 20px;
                color: white;
                font-size: 18px;
                font-weight: bold;
                text-align: center;
                min-height: 80px;
                transform: perspective(500px) rotateX(5deg);
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            }
        """)
        label7 = QLabel("RIDGE BORDER WITH CONICAL GRADIENT")
        label7.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label7.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        layout7 = QVBoxLayout(frame7)
        layout7.addWidget(label7)
        container_layout.addWidget(frame7)
        
        # Example 8: Inset Border with Opacity
        frame8 = QFrame()
        frame8.setStyleSheet("""
            QFrame {
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.5,
                                          stop:0 #1abc9c, stop:1 #16a085);
                border: 5px inset #2c3e50;
                border-radius: 10px;
                padding: 20px;
                color: white;
                font-size: 16px;
                font-weight: bold;
                text-align: center;
                min-height: 80px;
                opacity: 0.9;
                box-shadow: inset 0 0 30px rgba(0,0,0,0.3);
            }
            QFrame:hover {
                opacity: 1.0;
                transition: all 0.3s ease;
            }
        """)
        label8 = QLabel("INSET BORDER WITH OPACITY (HOVER TO SEE CHANGE)")
        label8.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label8.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        layout8 = QVBoxLayout(frame8)
        layout8.addWidget(label8)
        container_layout.addWidget(frame8)
        
        # Example 9: Outset Border with Scrollbar
        frame9 = QFrame()
        frame9.setStyleSheet("""
            QFrame {
                background-color: #ecf0f1;
                border: 5px outset #3498db;
                border-radius: 10px;
                padding: 20px;
                max-height: 150px;
                overflow: auto;
                scrollbar-width: thin;
                scrollbar-color: #3498db #ecf0f1;
            }
            QFrame::-webkit-scrollbar {
                width: 8px;
            }
            QFrame::-webkit-scrollbar-track {
                background: #ecf0f1;
                border-radius: 4px;
            }
            QFrame::-webkit-scrollbar-thumb {
                background: #3498db;
                border-radius: 4px;
            }
            QFrame::-webkit-scrollbar-thumb:hover {
                background: #2980b9;
            }
        """)
        label9 = QLabel(
            "OUTSET BORDER WITH SCROLLBAR\n"
            "This frame has vertical scrolling\n"
            "with custom scrollbar styling.\n"
            "Line 1\nLine 2\nLine 3\nLine 4\nLine 5\nLine 6"
        )
        label9.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label9.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 14px;
                font-weight: bold;
                line-height: 2;
            }
        """)
        layout9 = QVBoxLayout(frame9)
        layout9.addWidget(label9)
        container_layout.addWidget(frame9)
        
        # Example 10: All Border Styles Combined
        frame10 = QFrame()
        frame10.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #2c3e50, stop:1 #34495e);
                border: 2px solid #3498db;
                border-radius: 8px;
                padding: 20px;
                color: #ecf0f1;
                font-family: 'Courier New', monospace;
                font-size: 14px;
                font-weight: bold;
                text-align: center;
                min-height: 80px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3),
                           inset 0 2px 4px rgba(255,255,255,0.1);
                text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
                letter-spacing: 2px;
                word-spacing: 5px;
                text-transform: uppercase;
                cursor: pointer;
            }
            QFrame:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #34495e, stop:1 #2c3e50);
                border-color: #e74c3c;
                box-shadow: 0 6px 12px rgba(0,0,0,0.4);
                transform: scale(1.01);
                transition: all 0.3s ease;
            }
        """)
        label10 = QLabel("ALL PROPERTIES COMBINED\nHover to see effects")
        label10.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label10.setStyleSheet("color: #ecf0f1; font-size: 16px; font-weight: bold;")
        layout10 = QVBoxLayout(frame10)
        layout10.addWidget(label10)
        container_layout.addWidget(frame10)
        
        scroll.setWidget(container)
        main_layout.addWidget(scroll)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AllQSSPropertiesDemo()
    window.show()
    sys.exit(app.exec())