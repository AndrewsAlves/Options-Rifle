from PySide6.QtCore import QThread, Signal

class WorkerThread(QThread):
    finished = Signal(str)
    result = Signal()

    def __init__(self, func, *args, **kwargs):
        super(WorkerThread, self).__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        res = self.func(*self.args, **self.kwargs)
        self.finished.emit(res)