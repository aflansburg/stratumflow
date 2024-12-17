# paubox-cloud-functions

Repository for data platform Paubox related Cloud Functions.

## PubSub Topic to Cloud Function mapping

Many Cloud Functions will map and subscribe to PubSub Topics that receive a message directive from Google Cloud Scheduler. The Cloud Scheduler push to PubSub topic is the initial trigger that creates the message in the topic that the Cloud Function subscribes to.

Ensure the PubSub Topic & Cloud Scheduler job exist. See [this Terraform file](https://github.com/remohealth/terraform/blob/main/infra/app/data-platform/gcp/prod/paubox_pipeline.tf) in our Terraform repo.


TBD: Diagram

## Local Setup


## CI/CD

There is a tests workflow.

There is a deployment workflow.