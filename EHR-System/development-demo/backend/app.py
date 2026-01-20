import os
from flask import jsonify, Flask
from cassandra.cluster import Cluster
from cassandra.cluster import Cluster
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.management import sync_table, create_keyspace_simple
from cassandra.cqlengine import connection
from dotenv import load_dotenv

# Initialize
load_dotenv()
app = Flask(__name__)


# Get cluster based on deployment
if os.getenv("docker_deployment") == "true":
    cluster = Cluster(
        [
            "scylla-node1",
            "scylla-node2",
            "scylla-node3",
        ],
        port=9042,
    )
else:
    cluster = Cluster(
        [
            "127.0.0.1",
        ],
        port=9042,
    )

# Create connection using cluster session now using ORM
session = cluster.connect()
connection.set_session(session)

# Create and setkeyspace
create_keyspace_simple(
    "ehr_keyspace",
    replication_factor=3,
    connections=["default"]
)
session.set_keyspace("ehr_keyspace")

# Routes

@app.route("/")
def main_page():
    return "EHR System is running!!"




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)