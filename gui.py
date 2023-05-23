from random import random
from sys import argv, stderr
from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QMainWindow
from PySide6.QtGui import QColor, QPainter, QPolygonF, QResizeEvent
from PySide6.QtCore import Qt, QPointF
from srcs import *

def parse_args():
	if len(argv) != 2:
		print(f"Usage: {argv[0]} <number of parts>", file=stderr)
		exit(1)
	n = int(argv[1])
	if n < 2:
		raise ValueError("n must be at least 2")
	return n

rand_gen = random()
def random_color():
	global rand_gen
	rand_gen += 0.618033988749895
	rand_gen %= 1
	return QColor.fromHsvF(rand_gen, 0.5, 0.95)

if __name__ == "__main__":
	try:
		n = parse_args()
	except Exception as e:
		print(f"Error: {e}", file=stderr)
		exit(1)
	app = QApplication(argv)
	w = QMainWindow()
	w.setWindowTitle("N-Partitions")
	scene = QGraphicsScene()
	view = QGraphicsView(scene)
	view.setRenderHint(QPainter.Antialiasing)
	w.setCentralWidget(view)

	init = False
	def check_maximized(e: QResizeEvent):
		global init
		if not init and w.isMaximized():
			vsize = view.viewport().size()
			width, height = vsize.width(), vsize.height()
			polygons = nparts(width, height, n)
			for p in polygons:
				qtp = QPolygonF()
				[qtp.append(QPointF(v.x, v.y)) for v in p.vertices]
				scene.addPolygon(qtp, Qt.NoPen, random_color())
			scene.setSceneRect(0, 0, width, height)
			init = True
		view.fitInView(scene.sceneRect(), Qt.IgnoreAspectRatio)

	def esc_to_quit(e):
		if e.key() == Qt.Key_Escape:
			app.quit()
	w.keyPressEvent = esc_to_quit

	w.resizeEvent = check_maximized
	w.show()
	w.setWindowState(w.windowState() | Qt.WindowMaximized)
	app.exec()
