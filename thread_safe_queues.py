from queue import LifoQueue, PriorityQueue, Queue
from random import randint, choice
from time import sleep

from render_state import View

import argparse
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
        self.progress = 0

    @property
    def state(self):
        """Check the state of a worker thread and request that it
        simulate some work or idle time

        Returns(str):
        - product's name and the progress of work
        - indicating the worker is currently idle
        """
        if self.working:
            return f"{self.product} ({self.progress})%"
        return ":zzz: Idle"

    def simulate_idle(self):
        """Resets the state of a worker thread and goes to sleep
        for a random amount of seconds
        """
        self.product = None
        self.working = False
        self.progress = 0
        sleep(randint(1, 3))

    def simulate_work(self):
        """Pick a random delay in seconds adjusted to the worker's speed
        and progresses through the work
        """
        self.working = True
        self.progress = 0
        delay = randint(1, 1 + 15 // self.speed)
        for _ in range(100):
            sleep(delay / 100)
            self.progress += 1


class Producer(Worker):
    def __init__(self, speed, buffer, products):
        super().__init__(speed, buffer)
        self.products = products

    def run(self):
        """
        Producer works in an infinite loop, choosing a random product
        and simulating some worker b4 putting that product onto the queue
        called buffer
        """
        while True:
            self.product = choice(self.products)
            self.simulate_work()
            # put a product into the queue
            self.buffer.put(self.product)
            self.simulate_idle()


class Consumer(Worker):
    def run(self):
        """
        Works in an infinite loop, waiting for
        a product to appear in the queue.
        """
        while True:
            # .get() is blocking by default, which will keep the
            # consumer thread stopped and waiting until there's
            # at least one product in the queue

            # this way waiting consumer won't waster resources(CPU cycles)
            # while os allocates valuable resources to other threads
            # doing useful work
            self.product = self.buffer.get()
            self.simulate_work()
            # when we get something from a synchronized queue,
            # its internal counter increases to let other threads know
            # the queue hasn't been drained yet
            # so we should mark a dequeued task as done
            # unless we don't have any threads joining the queue
            # our_thread.join()
            self.buffer.task_done()  # decrease internal counter of queue
            self.simulate_idle()


def main(args):
    buffer = QUEUE_TYPES[args.queue]()
    producers = [
                    Producer(args.producer_speed, buffer, PRODUCTS)
                    for _ in range(args.producers)
                 ]
    consumers = [
                    Consumer(args.consumer_speed, buffer)
                    for _ in range(args.consumers)
                 ]

    for producer in producers:
        producer.start()

    for consumer in consumers:
        consumer.start()

    view = View(buffer, producers, consumers)
    view.animate()


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
