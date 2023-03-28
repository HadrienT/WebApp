import multiprocessing


def send_result(queue: multiprocessing.Queue, result: list[int]) -> None:  # type: ignore
    queue.put(result)
