from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.onprem.client import User
from diagrams.programming.framework import Django, React
from diagrams.programming.language import Python
from diagrams.onprem.database import PostgreSQL
from diagrams.generic.compute import Rack
from diagrams.saas.identity import Auth0
from diagrams.saas.cdn import Cloudflare

with Diagram("RAG AI Architecture", show=False):

    user = User("User")

    with Cluster("Vercel"):
        frontend = React("React + Vite")

    with Cluster("Authentication"):
        clerk = Auth0("Clerk JWT")

    with Cluster("AWS"):
        backend = Django("Django + DRF")
        vector = Python("VectorService\nSentenceTransformers")

    with Cluster("Supabase"):
        db = PostgreSQL("Postgres + pgvector\nknowledge_base")

    with Cluster("Modal.com"):
        llm_api = Python("FastAPI LLM Gateway")
        model = Rack("DeepSeek Model\nContainer")
        scraper = Python("Daily Scraper\nIngestion Job")

    user >> frontend
    frontend >> clerk
    frontend >> backend
    backend >> vector
    vector >> db
    backend >> llm_api
    llm_api >> model
    scraper >> db
    backend >> frontend
