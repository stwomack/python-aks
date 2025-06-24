import asyncio
import datetime
import logging
from temporalio.client import Client, WorkflowHandle

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from workflows import YourWorkflow

async def main():
    try:
        logging.info("Connecting to Temporal server...")
        client = await Client.connect("localhost:7233")
        logging.info("Successfully connected to Temporal server.")
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
                YourWorkflow.run,
                workflow_arg,
                id=workflow_id,
                task_queue="my-task-queue",
            )
            logging.info(f"Workflow {workflow_id} started. Run ID: {result_handle.result_run_id}")

        except Exception as e:
            logging.error(f"Failed to start workflow {workflow_id}: {e}")

        logging.info("Waiting 10 seconds before next workflow execution...")
        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())