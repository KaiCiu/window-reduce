import os
from quixstreams import Application
from datetime import timedelta

# for local dev, load env vars from a .env file
from dotenv import load_dotenv
load_dotenv()

# create a Quix Streams application
app = Application()

# JSON deserializers/serializers used by default
input_topic = app.topic(os.environ["input"])
output_topic = app.topic(os.environ["output"])

# consume from input topic
sdf = app.dataframe(input_topic)

# calculate average speed using 15 second tumbling window
sdf = sdf.apply(lambda row: row["Speed"]) \
    .tumbling_window(timedelta(seconds=15)).mean().final() \
        .apply(lambda value: {
            'average-speed': value['value'],
            'time': value['end']
            })

# print every row
sdf = sdf.update(lambda row: print(row))

# publish to output topic
sdf = sdf.to_topic(output_topic)

if __name__ == "__main__":
    app.run(sdf)