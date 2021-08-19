# This function is not intended to be invoked directly. Instead it will be
# triggered by an HTTP starter function.
# Before running this sample, please:
# - create a Durable activity function (default name is "Hello")
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import json
import requests

import azure.functions as func
import azure.durable_functions as df

def entity_function(context: df.DurableOrchestrationContext):

    logging.info(f"KEY: {str(context.entity_key)}")

    current_value = context.get_state(lambda: [])
    operation = context.operation_name
    if operation == "addSuffix":
        logging.info("Operation: addSuffix")
        amount = context.get_input()
        current_value.append(amount)
        context.set_result(current_value)
        logging.info(f"Value: {current_value}")
    # elif operation == "resetSuffix":
    #     current_value = []
    elif operation == "getSuffix":
        logging.info("Operation: getSuffix")
        context.set_result(current_value)
        logging.info(f"Value: {current_value}")
    
    context.set_state(current_value)

    if len(current_value) == 3:
        # Send to combine API
        # Write combined data tostorage table
        logging.info()

main = df.Entity.create(entity_function)



# {
#   "orderHeaderDetailsCSVUrl": "https://soh.blob.core.windows.net/six/XXXXXXXXXXXXXX-OrderHeaderDetails.csv",
#   "orderLineItemsCSVUrl": "https://soh.blob.core.windows.net/six/XXXXXXXXXXXXXX-OrderLineItems.csv",
#   "productInformationCSVUrl": "https://soh.blob.core.windows.net/six/XXXXXXXXXXXXXX-ProductInformation.csv"
# }

# new_dict = {}
# new_dict['orderHeaderDetailsCSVUrl'] = blob name
# Is dict sze 3?

# Send to aPI

# destroy on exit
