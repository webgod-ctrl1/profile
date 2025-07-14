import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QColor, QPainter, QBrush, QCursor, QFont
from PyQt5.QtCore import Qt, QTimer, QPointF
import random
import math

class Particle:
    def __init__(self, width, height):
        self.x = random.uniform(0, width)
        self.y = random.uniform(0, height)
        self.radius = random.uniform(2, 5)
        self.color = QColor(200, 200, 255, 180)
        self.speed = random.uniform(0.5, 2)
        self.angle = random.uniform(0, 2 * math.pi)

    def move(self, width, height, cursor_pos=None):
        # If cursor is near, move away
        if cursor_pos:
            dx = self.x - cursor_pos.x()
            dy = self.y - cursor_pos.y()
            dist = math.hypot(dx, dy)
            if dist < 80:
                angle = math.atan2(dy, dx)
                self.x += math.cos(angle) * 2
                self.y += math.sin(angle) * 2
        # Normal movement
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        # Wrap around
        if self.x < 0: self.x = width
        if self.x > width: self.x = 0
        if self.y < 0: self.y = height
        if self.y > height: self.y = 0

class ParticleWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.particles = []
        self.setMouseTracking(True)
        self.cursor_pos = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_particles)
        self.timer.start(16)
        self.init_particles()

    def init_particles(self):
        self.particles = [Particle(self.width(), self.height()) for _ in range(60)]

    def resizeEvent(self, event):
        self.init_particles()

    def mouseMoveEvent(self, event):
        self.cursor_pos = event.pos()

    def leaveEvent(self, event):
        self.cursor_pos = None

    def update_particles(self):
        for p in self.particles:
            p.move(self.width(), self.height(), self.cursor_pos)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(30, 30, 60))
        # Draw lines between close particles
        for i, p1 in enumerate(self.particles):
            for p2 in self.particles[i+1:]:
                dist = math.hypot(p1.x - p2.x, p1.y - p2.y)
                if dist < 80:
                    alpha = int(120 * (1 - dist / 80))
                    painter.setPen(QColor(180, 180, 255, alpha))
                    painter.drawLine(QPointF(p1.x, p1.y), QPointF(p2.x, p2.y))
        # Draw particles
        for p in self.particles:
            painter.setBrush(QBrush(p.color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPointF(p.x, p.y), p.radius, p.radius)

class PortfolioUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Portfolio")
        self.setGeometry(100, 100, 900, 600)
        self.particle_bg = ParticleWidget(self)
        self.particle_bg.setGeometry(0, 0, 900, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()
        title = QLabel("Your Name")
        title.setStyleSheet("color: white;")
        title.setFont(QFont("Arial", 32, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        subtitle = QLabel("Software Developer | Portfolio")
        subtitle.setStyleSheet("color: #b0b0ff;")
        subtitle.setFont(QFont("Arial", 18))
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()
        self.setLayout(layout)

    def resizeEvent(self, event):
        self.particle_bg.setGeometry(0, 0, self.width(), self.height())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PortfolioUI()
    window.show()
    sys.exit(app.exec_())