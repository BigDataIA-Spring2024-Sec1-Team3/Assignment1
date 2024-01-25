from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda, EC2
from diagrams.aws.database import Redshift
from diagrams.aws.storage import S3
from diagrams.programming.language import Python
from diagrams.onprem.container import Docker
from diagrams.aws.network import ELB
from diagrams.aws.compute import EKS
from diagrams.custom import Custom


with Diagram("ETL Data Pipeline", show=True):
    airflow = Custom("Airflow\nAirflow is used to\nmanage DAGs through out\nETL process","./part2/airflow.png")
    with Cluster("Data Extraction"):
        user_data = Custom("LinkedIn's Profile API\nallows to retrieve\ndata from\nLinkedIn profiles","./part2/linkedin.png")
        job_listings = Custom("BeautifulSoup\nJobs data from \nvarious websites is\nobtained through\nweb scraping", "./part2/indeed.png")

        raw_data_storage = S3("Amazon S3 Bucket\nis used as stage\nto store raw\ndata temperorily.")
        airflow >> user_data >> Edge(label="LinkedIn users data") >> raw_data_storage
        airflow >> job_listings >> Edge(label="Scraped jobs") >> raw_data_storage

    with Cluster("Data Transformation"):
        processing_tools = Python("Python is used\nto process the\nraw data and load\nto AWS Redshift.")
        raw_data_storage >> processing_tools
    
    with Cluster("Data Load"):
        data_warehouse = Redshift("Amazon Redshift\nserves as the\ndata warehouse for\nstoring & analyzing\nprocessed data")
        processing_tools >> data_warehouse