from flask import jsonify, Flask
from cassandra.cluster import Cluster
from cassandra.cluster import Cluster
import os
import time

app = Flask(__name__)

# Create this dynamically based on environment vars
cluster = Cluster(
    [
        "scylladb-0.scylladb.scylladb.svc.cluster.local",
        "scylladb-1.scylladb.scylladb.svc.cluster.local",
        "scylladb-2.scylladb.scylladb.svc.cluster.local",
    ],
    port=9042,
)

session = cluster.connect()
session.set_keyspace("ehr_keyspace")

# TODO Create keyspace and use correct replication strategy

@app.route("/")
def main_page():
    return "EHR System is running!!"

# TODO not secure, just for testing!
@app.route("/get/<table_name>", methods=["GET"])
def get_rows(table_name):
    cql = f"SELECT * FROM {table_name}"
    rows = session.execute(cql)
    result = [dict(row._asdict()) for row in rows]
    return jsonify(result), 200

# TODO add HTTPS and basic auth

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)