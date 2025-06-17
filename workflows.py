from datetime import timedelta
from temporalio import workflow

@workflow.defn
class YourWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        return await workflow.execute_activity(
            your_first_activity,
            name,
            start_to_close_timeout=timedelta(seconds=10),
        )

your_workflow = YourWorkflow