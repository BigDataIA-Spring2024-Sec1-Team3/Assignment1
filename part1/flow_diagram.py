from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda, EC2
from diagrams.aws.database import Redshift
from diagrams.aws.storage import S3
from diagrams.programming.language import Python
from diagrams.onprem.container import Docker
from diagrams.aws.network import ELB
from diagrams.aws.compute import EKS
from diagrams.custom import Custom


with Diagram("Architecture", show=True):
    with Cluster("Job Recommendation Application"):
        airflow = Custom("Airflow","./part1/airflow.png")
        with Cluster("Data Collection"):
            user_data = Custom("Profile API","./part1/linkedin.png")
            job_listings = Custom("BeautifulSoup", "./part1/indeed.png")

            raw_data_storage = S3("Amazon S3 Buckets")
            airflow >> user_data >> Edge(label="LinkedIn users data") >> raw_data_storage
            airflow >> job_listings >> Edge(label="Jobs Scraping - Indeed, Glassdoor") >> raw_data_storage

        with Cluster("Data Preprocessing and Storage"):
            processing_tools = Python("Processing")
            data_warehouse = Redshift("Amazon Redshift")
            raw_data_storage >> processing_tools >> data_warehouse
            

        with Cluster("Machine Learning Modeling"):
            ml_environment = Python("Recommendation System")
            model_storage = S3("Trained Models in S3")

            data_warehouse >> ml_environment >> model_storage
        
    with Cluster("containerization"):
        backend_framework = Docker("Docker")       
        model_storage >> backend_framework


    with Cluster("Deployment"):
        container_orchestration = EKS("Kubernetes")
        ec2_server = EC2("EC2 Server")
        backend_framework  >> container_orchestration >> ec2_server
        

    ui = Custom("User Interface","./part1/ui.png")
    ec2_server >> ui
    ui >> ec2_server