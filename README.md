# StratumFlow

![Deploy Cloud Function](https://github.com/remohealth/cloudfunctions/actions/workflows/deploy_cloud_function.yml/badge.svg)

A practical and layered approach to handling cloud native job execution.

Read more:
- [Notion Web](https://www.notion.so/remohealth/StratumFlow-165778a1a81b80a38f53c1968a33cba9?pvs=4)

<img src="assets/stratumflow.jpg" alt="Cloud Function Flow" width="650"/>

## PubSub Topic to Cloud Function mapping

Many Cloud Functions will map and subscribe to PubSub Topics that receive a message directive from Google Cloud Scheduler. The Cloud Scheduler push to PubSub topic is the initial trigger that creates the message in the topic that the Cloud Function subscribes to.

Ensure the PubSub Topic & Cloud Scheduler job exist. See [this Terraform file](https://github.com/remohealth/terraform/blob/main/infra/app/data-platform/gcp/prod/paubox_pipeline.tf) in our Terraform repo.

## Example Paubox use case for Cloud Functions

<img src="assets/flow.jpg" alt="Cloud Function Flow" width="650"/>

## Local Setup

1. Make sure you have [uv](https://docs.astral.sh/uv/)
2. Clone the repo
3. Create virtual environment with `uv venv `.
4. Activate the virtual environment with `source .venv/bin/activate`
5. Install the project's pinned Python version with `uv python install`
6. Install all deps with `uv sync --all-extras --dev`
7. Run tests locally with `uv run pytest ./tests`

## CI/CD

There is a tests workflow.

There is a deployment workflow.
