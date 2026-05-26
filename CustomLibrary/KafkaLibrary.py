from robot.api.deco import keyword
from kafka import kafkaConsumer

class KafkaLibrary(object):
    def __init__(self):
        self.consumer = None

    @keyword
    def connect_to_kafka(self, server):
        self.consumer = KafkaConsumer(bootstrap_servers=server)

    @keyword
    def fetch_kafka_logs(self, topic):
        self.consumer.subscribe([topic])
        logs = []
        for message in self.consumer:
            logs.append(message)
        return logs
    
    @keyword
    def disconnect_from_kafka(self):
        self.consumer.close()
