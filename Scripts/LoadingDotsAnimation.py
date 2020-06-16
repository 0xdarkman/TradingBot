import itertools
import threading
import time
import sys

stop_animate = False


def animate_loading(LOADING_TEXT="Loading", DONE_TEXT="Done!"):
	global stop_animate
	stop_animate = False

	def animate():
		for c in itertools.cycle(['.', '..', '...', '....', '.....', '......']):
			if stop_animate:
				break
			sys.stdout.write('\r' + LOADING_TEXT + c)
			sys.stdout.flush()
			time.sleep(0.25)
		sys.stdout.write('\r' + DONE_TEXT + '\n')

	t = threading.Thread(target=animate)
	t.start()


animate_loading(LOADING_TEXT="KJSAFDHKFJA")
time.sleep(3)
stop_animate = True
print("yiyiyiyiy")

animate_loading(LOADING_TEXT="Logging out", DONE_TEXT="Successfully logged out!")
time.sleep(3)
stop_animate = True
