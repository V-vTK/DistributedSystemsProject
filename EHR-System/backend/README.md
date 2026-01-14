
ScyllaDB is statefulset and this is deployment (can autoscale). We would need scyllaDB operator deployed with Helm to autoscale scyllaDB.
https://spacelift.io/blog/statefulset-vs-deployment#stateful-vs-stateless-applications

docker build -t flask-scylla:v1 .
docker run -p 5000:5000 flask-scylla:v1 #  Had trouble with latest tag, it did not reload the newest image...
minikube image load flask-scylla:latest #  load to minikube otherwise not available

kubectl apply -f flask-scylla-deployment.yaml

kubectl get pods -n scylladb
kubectl get svc -n scylladb



kubectl port-forward svc/flask-scylla 5000:5000 -n scylladb # Kubernetes (minikube) does not expose like docker, requires a tunnel to between host and minikube

kubectl delete pod -l app=flask-scylla -n scylladb

Some logs from manual testing (surprisingly difficult to get the connections (Flask -> ScyllaDB) working...):

root@flask-scylla-7bf8d75595-7dvmx:/app# python
>>> cluster2 = Cluster([
...   "scylladb-0.scylladb.scylladb.svc.cluster.local",
...   "scylladb-1.scylladb.scylladb.svc.cluster.local",
...   "scylladb-2.scylladb.scylladb.svc.cluster.local",
... ], port=9042)
>>> session = cluster2.connect()
>>> session.set_keyspace("ehr_keyspace")
>>> rows = session.execute("SELECT * FROM patients")
>>> print(rows)
<cassandra.cluster.ResultSet object at 0x7faacc726dd0>
>>> print(list(rows))
[Row(id=1, age=45, diagnosis='Hypertension', name='John Doe')]

The database is currently created manually with exec, see scylla_db readme.