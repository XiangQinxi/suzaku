import time
import threading
import heapq
from typing import Callable, Optional


class AfterScheduler:
    """完全独立实现的定时任务调度器，模拟 tkinter.after 功能"""

    def __init__(self):
        self._tasks = []
        self._counter = 0
        self._lock = threading.Lock()
        self._running = True
        self._thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self._thread.start()

    def after(self, delay_ms: int, callback: Callable, *args) -> str:
        """
        安排延迟执行的任务
        :param delay_ms: 延迟毫秒数
        :param callback: 回调函数
        :param args: 回调参数
        :return: 任务ID (可用于取消)
        """
        with self._lock:
            task_id = f"task_{self._counter}"
            heapq.heappush(
                self._tasks,
                (time.monotonic() + delay_ms / 1000, self._counter, task_id, callback,
                 args)
            )
            self._counter += 1
            return task_id

    def cancel(self, task_id: str) -> None:
        """取消已安排的任务"""
        with self._lock:
            for i, task in enumerate(self._tasks):
                if task[2] == task_id:
                    self._tasks.pop(i)
                    heapq.heapify(self._tasks)  # 重新堆化
                    break

    def _run_scheduler(self) -> None:
        """调度器主循环"""
        while self._running:
            with self._lock:
                now = time.monotonic()
                while self._tasks and self._tasks[0][0] <= now:
                    _, _, _, callback, args = heapq.heappop(self._tasks)
                    try:
                        callback(*args)
                    except Exception as e:
                        print(f"Task error: {e}")

            time.sleep(0.01)  # 降低CPU占用

    def destroy(self) -> None:
        """停止调度器并清理资源"""
        with self._lock:
            self._running = False
            self._tasks.clear()

    def __del__(self):
        self.destroy()


# 使用示例
if __name__ == "__main__":
    scheduler = AfterScheduler()


    def say_hello(name: str):
        print(f"Hello {name}! Time: {time.time():.2f}")


    # 安排3个任务
    task1 = scheduler.after(1000, say_hello, "Alice")  # 1秒后执行
    task2 = scheduler.after(2000, say_hello, "Bob")  # 2秒后执行
    #scheduler.after(1500, lambda: scheduler.cancel(task2))  # 1.5秒后取消task2

    # 保持主线程运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.destroy()
