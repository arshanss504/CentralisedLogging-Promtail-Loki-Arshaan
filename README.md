# CentralisedLogging-Promtail-Loki-Arshaan

I have created a mock service that writes logs into a local filesystem. Promtail agent is configured to scrape logs from that filepath and export it to Loki. User can visualise logs in Grafana by adding Loki as a data source.

Includes Docker Compose file inside. Make sure the required ports are NOT in use already.
Main service is not dockerized, you have to run it using the command- $ uvicorn main:app --reload

User is free to create custom image of the service.

