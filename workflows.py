from datetime import timedelta
from temporalio import workflow

from activities import your_first_activity, your_second_activity, your_third_activity

@workflow.defn
class YourWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        await workflow.execute_activity(
            your_first_activity,
            name,
            start_to_close_timeout=timedelta(seconds=10),
        )
        await workflow.execute_activity(
            your_second_activity,
            name,
            start_to_close_timeout=timedelta(seconds=10),
        )
        return await workflow.execute_activity(
            your_third_activity,
            name,
            start_to_close_timeout=timedelta(seconds=10),
        )

your_workflow = YourWorkflow