def function_handler(function_input):
    pass


# import logging
#
#
# def function_handler(function_input):
#    logging.info(function_input)
#    logging.info(type(function_input))
#
#    payload = function_input["payload"]
#    logging.info(payload)
#    logging.info(type(payload))
#
#    # Convert str to bytes
#    payload = payload.decode("utf-8")
#    logging.info(payload)
#    logging.info(type(payload))
#
#    metadata_map = function_input["metadata_map"]
#    logging.info(metadata_map)
#    logging.info(type(metadata_map))
#
#    logging.info(metadata_map["a"])
#    logging.info(type(metadata_map["a"]))
#
#    return {"result": 42}
