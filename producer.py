from flask import Flask, Response, request
from kafka import SimpleProducer, KafkaClient
#  connect to Kafka
kafka = KafkaClient('localhost:9092')
producer = SimpleProducer(kafka)
# Assign a topic
topic = 'messages'


# Continuously listen to the connection and print messages as recieved
app = Flask(__name__)


@app.route('/analytics')
def index():
    x = request.args.get('x', type=int)
    y = request.args.get('y', type=int)
    msg = 'X: {};  Y: {}'.format(x, y)
    producer.send_messages('mouse', msg.encode())
    return Response('OK',
                    content_type='text/plain; charset=utf-8')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
