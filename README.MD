Distributed systems course topic 2026

Healthcare data often resides in siloed systems, making it difficult to unify patient records. Build a secure, distributed EHR system allowing multiple hospitals to share patient data while preserving privacy. Key technical novelties include: consensus and replication strategies for ensuring data integrity across facilities. Main challenge would in ensuring interoperability and reliability in a distributed environment for EHR setting.

Key Increments (6-Week Outline): 
1. Introduction: Single hospital EHR with basic Create, Read, Update, and Delete (CRUD) for patient data.

2. Communication: Enable secure inter-hospital data exchange.

3. Time & Consensus: Keep records consistent with distributed consensus (Raft/Paxos).

4. Non-Functional Reqs: Ensure system can handle large spikes in data queries while maintaining low latency.

5. Replication & Consistency: Redundant storage across hospitals.

6. Resource Management & Scheduling: Efficient data synchronization tasks.

7. Architecture: Microservices for patient records, audit logs, identity & access management.

8. Middleware: Data encryption, compliance checks, logging.

9. Datacenter & Cloud: Possibly private cloud for healthcare data.

10. Big Data Processing: Analyze aggregated EHR data for population health insights.

11. Distributed ML: Predict patient risks or readmissions across hospitals in real time.

12. Edge–Cloud Continuum: Local clinics act as edge nodes, synchronizing with central cloud stores.