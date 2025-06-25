import asyncio
import os

from temporalio.worker import Worker
from temporalio.client import Client

from workflows import your_workflow
from activities import your_first_activity, your_second_activity, your_third_activity
from config import TEMPORAL_ADDRESS, TEMPORAL_NAMESPACE, TEMPORAL_TASK_QUEUE, TEMPORAL_API_KEY, KEYVAULT_URL, KEYVAULT_SECRET_NAME
from crypto_converter import encrypted_converter

async def main():
    # For local development, connect without TLS or API key
    if TEMPORAL_ADDRESS.startswith("localhost") or "host.docker.internal" in TEMPORAL_ADDRESS:
        client = await Client.connect(
            TEMPORAL_ADDRESS,
            namespace=TEMPORAL_NAMESPACE,
            data_converter=encrypted_converter
        )
    else:
        # For Temporal Cloud, use TLS and API key
        client = await Client.connect(
            TEMPORAL_ADDRESS,
            namespace=TEMPORAL_NAMESPACE,
            rpc_metadata={"temporal-namespace": TEMPORAL_NAMESPACE},
            api_key=TEMPORAL_API_KEY,
            tls=True,
            data_converter=encrypted_converter
        )
    
    print("Initializing worker...")
    # Initialize the worker
    worker = Worker(
        client,
        task_queue=TEMPORAL_TASK_QUEUE,
        workflows=[your_workflow],
        activities=[
            your_first_activity,
            your_second_activity,
            your_third_activity
        ]
    )

    print("Starting worker... Awaiting tasks.")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())