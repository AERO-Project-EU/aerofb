import time

from flask import Flask, request

app = Flask(__name__)


@app.post("/invoke")
def invoke():
    start_ts = time.perf_counter_ns()
    app.logger.debug("New invocation request...")
    function_input = request.get_json(force=True)
    app.logger.debug(f"function_input: {function_input}")

    global function_handler
    if "function_handler" not in globals():
        from function_handler import function_handler
    function_output = function_handler(function_input)

    return {
        "duration_ns": time.perf_counter_ns() - start_ts,
        "output": str(function_output),
    }
