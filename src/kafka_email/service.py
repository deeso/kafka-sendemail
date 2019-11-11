from multiprocessing import Pool
from .consts import *
from .actions import KafkaConsumer
from .config import Config
import asyncio
import threading
import asyncio

#TODO create the config parser
#TODO start/stop consumers (as a process pool?) for this service
#TODO add asyncio or eventlets with consumer

class EmailSenderService(object):

    def __init__(self, num_processes=DEFAULT_NUM_PROCESSES, consumer_config=None, producer_config=None, email_config=None):
        self.num_processes = num_processes
        self.producer_config = producer_config
        self.consumer_config = consumer_config
        self.component_type = Config.CONFIG[KAFKA_COMPONENT]

        if self.consumer_config is None:
            self.consumer_config = DEFAULT_KAFKA_CONFIG.copy()

        self.email_config = email_config
        self.consumer = KafkaConsumer(email_config=self.email_config, **self.consumer_config)
        self.keep_running = False
        self.consumer_thread = None
        self.producer_thread = None
        self.consumer_processes = []

    @classmethod
    def from_config(cls):
        num_process = Config.CONFIG.get(NUM_PROCESSES, DEFAULT_NUM_PROCESSES)
        consumer_config = Config.CONFIG.get(CONSUMER_CONFIG, DEFAULT_KAFKA_CONFIG.copy())
        producer_config = Config.CONFIG.get(CONSUMER_CONFIG, DEFAULT_KAFKA_CONFIG.copy())
        email_config = Config.CONFIG.get(EMAIL_CONFIG, DEFAULT_EMAIL_CONFIG.copy())

        return cls(num_processes=num_process,
                   consumer_config=consumer_config,
                   producer_config=producer_config,
                   email_config=email_config)

    def run(self):
        return self.start()

    def start(self):
        self.keep_running = True
        if self.component_type == CONSUMER:
            self.consumer.start()

            # self.consumer_thread_worker()


    def stop(self):

        if not self.keep_running:
            return
        self.keep_running = False
        if self.component_type == CONSUMER and not self.consumer_thread is None:
            self.consumer.stop()

        elif self.component_type == PRODUCER and not self.producer_thread is None:
            pass



    def _producer_thread(self):
        self.producer_thread = None

    async def consumer_thread_worker(self):
        self.keep_running = True
        while self.keep_running:
            eml = await self.consumer.receive()
            self.consumer.mp_email_message(eml)
