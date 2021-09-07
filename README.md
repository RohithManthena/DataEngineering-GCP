# DataEngineering-GCP

Idea - 1
Automating Cloud SQL store data syncronization with Google Big Query using Cloud Composer
Used MySQL classicmodels database


## Security Aspects
Cloud composer environment with VPC-native (default VPC) and private GKE Cluster. <br />
Private Cloud SQL Instance. <br />
VPC Peering connection betwwen Cloud SQL and Cloud Composer environment. <br />
Connection to cloud sql happens only through proxy server.<br />
To encrypt the connections I used cloud SQL proxy. Proxy client and Proxy server<br />




Idea - 2
Ingesting data from an API to GCS using pub/sub.
