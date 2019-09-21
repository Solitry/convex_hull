import threading
import time


class TestThread(threading.Thread):
    def __init__(self):
        super().__init__()
    
    def run(self):
        for _ in range(100):
            print("hahahah")


if __name__ == "__main__":
    test_thread = TestThread()

    test_thread.start()

    if test_thread.is_alive():
        print('here')
    else:
        print('here2')

    test_thread.join(0)
