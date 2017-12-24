from flask import Flask, Response
from kafka import SimpleProducer, KafkaClient
#  connect to Kafka
kafka = KafkaClient('localhost:9092')
producer = SimpleProducer(kafka)
# Assign a topic
topic = 'my-topic'


# Continuously listen to the connection and print messages as recieved
app = Flask(__name__)


@app.route('/')
def index():
    # return a multipart response
    producer.send_messages(topic, 'test')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
