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

## References

https://medium.com/@kolban1/cloud-composer-launching-dataflow-pipelines-38cd29e970d4                              <br />
https://medium.com/datareply/realtime-streaming-data-pipeline-using-google-cloud-platform-and-bokeh-9dd0cfae647a  <br />
https://medium.com/zenofai/machine-learning-operations-mlops-pipeline-using-google-cloud-composer-a8ebcbd6d766    <br />
https://medium.com/bakdata/data-warehousing-made-easy-with-google-bigquery-and-apache-airflow-bf62e6c727ed        <br />
https://towardsdatascience.com/scraping-reddit-data-1c0af3040768                                                  <br />
https://towardsdatascience.com/automate-your-cloud-sql-data-synchronization-to-bigquery-with-airflow-7f9d992da18f <br />
