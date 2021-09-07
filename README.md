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







Before we can create a private cloud SQL instance, we need to create a VPC (Virtual Private Cloud) peering connection between a VPC network in the GCP project (here we choose the ‘default’ VPC network) and the VPC network in which the cloud SQL instance resides. Instances on the ‘default’ network will then be able to connect to the private Cloud SQL instance using that VPC peering connection. 
