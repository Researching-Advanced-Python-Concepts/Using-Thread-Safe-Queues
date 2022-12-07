import argparse
from queue import LifoQueue, PriorityQueue, Queue
import threading

QUEUE_TYPES = {
    "fifo": Queue,
    "lifo": LifoQueue,
    "heap": PriorityQueue
    # python follows min heap property
}

# rich can replace these with corresponding emoji glyphs
# python -m rich.emoji
PRODUCTS = (
    ":balloon:",
    ":cookie:",
    ":crystal_ball:",
    ":diving_mask:",
    ":flashlight:",
    ":gem:",
    ":gift:",
    ":kite:",
    ":party_popper:",
    ":postal_horn:",
    ":ribbon:",
    ":rocket:",
    ":teddy_bear:",
    ":thread:",
    ":yo-yo:",
)


class Worker(threading.Thread):
    # our threads (consumer and producer) share a wealth of attributes
    # and behaviours, we encapsulate in a common base class
    def __init__(self, speed, buffer):
        # daemon run in background and close when the program ends
        # we don't need to end the thread and it won't prevent from
        # exiting when main thread finishes
        super().__init__(daemon=True)
        self.speed = speed
        self.buffer = buffer
        self.product = None
        self.working = False
        self.progrss = 0


def main(args):
    buffer = QUEUE_TYPES[args.queue]()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--queue", choices=QUEUE_TYPES, default="fifo")
    parser.add_argument("-p", "--producers", type=int, default=3)
    parser.add_argument("-c", "--consumers", type=int, default=3)
    parser.add_argument("-ps", "--producer-speed", type=int, default=1)
    parser.add_argument("-cs", "--consumer-speed", type=int, default=1)
    
    return parser.parse_args()


if __name__ == "__main__":
    try:
        main(parse_args())
    except KeyboardInterrupt:
        pass