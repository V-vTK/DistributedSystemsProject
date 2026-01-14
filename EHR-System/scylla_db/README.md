# Start up

start --cpus 6 --memory 15G
minikube dashboard

kubectl create namespace scylladb # Once

kubectl apply -f scylladb-statefulset.yaml -n scylladb

kubectl get pods -n scylladb

## Logs for one container:
kubectl logs scylladb-0 -n scylladb

## Describe cluster:
kubectl describe statefulset -n scylladb

Scale up and down:

kubectl scale statefulset scylladb --replicas=0 -n scylladb

kubectl scale statefulset scylladb --replicas=3 -n scylladb

Access shell
kubectl exec -it scylladb-0 -n scylladb -- /bin/bash

Create db table
CREATE KEYSPACE ehr_keyspace WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 3};


Edit cluster: (did not work correctly...)
kubectl edit statefulset scylladb -n scylladb


## Clean up / Delete

## Delete the statefulset, service, and pods. Will not delete data. 
kubectl delete statefulset scylladb -n scylladb
kubectl delete svc scylladb -n scylladb

## If you want to preserve the data, do not delete the PV and PVC.
## Instead, just delete the deployment and redeploy when ready,
## and start using your data.
## kubectl delete -f scylladb-statefulset.yaml -n scylladb

## To redeploy the statefulset with preserved data, use the following command:
## kubectl apply -f scylladb-statefulset.yaml -n scylladb

## If data preservation is not required, delete both PV and PVC
kubectl delete pvc -l app=scylladb -n scylladb
kubectl delete pv -l app=scylladb -n scylladb

# Sources:

https://medium.com/@sjksingh/deploy-a-persistent-scylladb-cluster-on-minikube-11495c1f5582
https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/
https://stackoverflow.com/questions/55446333/how-can-i-expose-a-statefulset-service-with-clusterip-none-on-google-cloud-platf


# Creating db table and keyspace

kubectl exec -it scylladb-0 -n scylladb -- /bin/bash #  (exec command)

Nodetool:
        nodetool help
CQL Shell:
        cqlsh
More documentation available at: 
        http://www.scylladb.com/doc/

root@scylladb-0:/# cqlsh
Connected to  at 10.244.0.122:9042.
[cqlsh 5.0.1 | Cassandra 3.0.8 | CQL spec 3.3.1 | Native protocol v4]
Use HELP for help.
cqlsh> DESCRIBE TABLES;
...

CREATE KEYSPACE ehr_keyspace WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 3};
cqlsh> CREATE TABLE IF NOT EXISTS patients (
   ...     id int,
   ...     name text,
   ...     age int,
   ...     diagnosis text,
   ...     PRIMARY KEY (id)
   ... );

cqlsh> USE ehr_keyspace;

cqlsh:ehr_keyspace> INSERT INTO patients (id, name, age, diagnosis)

cqlsh:ehr_keyspace> INSERT INTO patients (id, name, age, diagnosis) VALUES (1, 'John Doe', 34, 'Fever');
cqlsh:ehr_keyspace> SELECT * FROM patients;

 id | age | diagnosis    | name
----+-----+--------------+----------
  1 |  34 | Fever        | John Doe