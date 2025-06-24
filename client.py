import asyncio
import datetime
import logging
from temporalio.client import Client, WorkflowHandle

from workflows import your_workflow
from config import TEMPORAL_ADDRESS, TEMPORAL_NAMESPACE, TEMPORAL_TASK_QUEUE, TEMPORAL_API_KEY

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def main():
    try:
        logging.info("Connecting to Temporal server...")
        
        # For local development, connect without TLS or API key
        if TEMPORAL_ADDRESS.startswith("localhost") or "host.docker.internal" in TEMPORAL_ADDRESS:
            client = await Client.connect(
                TEMPORAL_ADDRESS,
                namespace=TEMPORAL_NAMESPACE
            )
        else:
            # For Temporal Cloud, use TLS and API key
            client = await Client.connect(
                TEMPORAL_ADDRESS,
                namespace=TEMPORAL_NAMESPACE,
                rpc_metadata={"temporal-namespace": TEMPORAL_NAMESPACE},
                api_key=TEMPORAL_API_KEY,
                tls=True
            )
            
        logging.info(f"Successfully connected to Temporal server at {TEMPORAL_ADDRESS} in namespace {TEMPORAL_NAMESPACE}.")
    except Exception as e:
        logging.error(f"Failed to connect to Temporal server: {e}")
        return

    workflow_counter = 0
    while True:
        workflow_counter += 1
        workflow_id = f"your-workflow-{workflow_counter}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        workflow_arg = f"ClientTriggeredPayload-{workflow_counter}"

        try:
            logging.info(f"Starting workflow with ID: {workflow_id} and argument: {workflow_arg}...")
            result_handle: WorkflowHandle[str] = await client.start_workflow(
                your_workflow.run,
                workflow_arg,
                id=workflow_id,
                task_queue=TEMPORAL_TASK_QUEUE,
            )
            logging.info(f"Workflow {workflow_id} started. Run ID: {result_handle.result_run_id}")

        except Exception as e:
            logging.error(f"Failed to start workflow {workflow_id}: {e}")

        logging.info("Waiting 10 seconds before next workflow execution...")
        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())