# DataEngineering-GCP

Idea - 1
Automating Cloud SQL store data syncronization with Google Big Query using Cloud Composer


Security Aspects
  Cloud composer environment with VPC-native (default VPC) and private GKE Cluster. 
  Private Cloud SQL Instance.
  VPC Peering connection betwwen Cloud SQL and Cloud Composer environment. 
  Connection to cloud sql happens only through proxy server.
  To encrypt the connections I used cloud SQL proxy. Proxy client and Proxy server

Data
MySQL classicmodels database






Before we can create a private cloud SQL instance, we need to create a VPC (Virtual Private Cloud) peering connection between a VPC network in the GCP project (here we choose the ‘default’ VPC network) and the VPC network in which the cloud SQL instance resides. Instances on the ‘default’ network will then be able to connect to the private Cloud SQL instance using that VPC peering connection. 
