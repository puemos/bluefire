from flask import Flask, Response
from kafka import KafkaConsumer

from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
import numpy as np
import re


def plot(x, y):
    plt.subplot(121)
    counts, xbins, ybins, image = plt.hist2d(
        x, y, bins=100, norm=LogNorm(), range=[[0, 1000], [0, 600]])
    plt.colorbar()
    plt.subplot(122)
    plt.contour(counts.transpose(), extent=[xbins[0], xbins[-1], ybins[0], ybins[-1]],
                linewidths=3, levels=[1, 5, 10, 25, 50, 70, 80, 100])


# connect to Kafka server and pass the topic we want to consume
consumer = KafkaConsumer('mouse', group_id='view',
                         bootstrap_servers=['0.0.0.0:9092'])

# Continuously listen to the connection and print messages as recieved
app = Flask(__name__)


@app.route('/')
def index():
    # return a multipart response

    return Response(kafkastream())


def kafkastream():
    x = []
    y = []
    regex = r"^b'X: ([0-9]*);  Y: ([0-9]*)"

    for response in consumer:
        matches = re.match(regex, str(response.value))
        x.append(matches.group(1))
        y.append(matches.group(2))
        if len(y) > 1000:
            return x, y


def run():
    x, y = kafkastream()
    x = np.array(x, np.int32)
    y = np.array(y, np.int32)
    plot(x, y)
    plt.show()


if __name__ == '__main__':
    run()
    # app.run(host='0.0.0.0', debug=True, port=8080)
