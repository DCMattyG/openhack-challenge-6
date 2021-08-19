# This function an HTTP starter function for Durable Functions.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable activity function (default name is "Hello")
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt
 
import logging
import re

import azure.functions as func
import azure.durable_functions as df

async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:
    client = df.DurableOrchestrationClient(starter)
    logging.info(f"Method: {req.method}")

    if req.method == "POST":
        body = req.get_json()
        file_name = body['fileName']
        regex_results = re.search(r'([0-9]{14})-(OrderHeaderDetails|OrderLineItems|ProductInformation).csv', file_name)
        file = regex_results.group(0)
        prefix = regex_results.group(1)
        suffix = regex_results.group(2)
        logging.info(f"Prefix: {prefix} | Suffix: {suffix}")
        entity_id = df.EntityId("Challenge6Entity", prefix)

        instance_id = await client.signal_entity(entity_id, "addSuffix", suffix)
    elif req.method == "GET":
        key = req.params.get('entityKey')
        entity_id = df.EntityId("Challenge6Entity", key)
        instance_id = await client.signal_entity(entity_id, "getSuffix", None)
        logging.info(f"RESULT: {instance_id}")

    return func.HttpResponse("Entity signaled")
