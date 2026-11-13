import json
from jsonschema import validate


def _strip_code_fence(text):
    # Models often wrap JSON in a Markdown code fence (```json ... ```). Remove one surrounding fence, if present.
    stripped = text.strip()
    if stripped.startswith("```") and stripped.endswith("```"):
        first_newline = stripped.find("\n")
        if first_newline != -1:
            return stripped[first_newline + 1 : -3].strip()
    return text


# Parse the JSON response string into an object and validate it against the JSON schema.
# Return the validated object.
# Implements: SW-REQ-001
# Implements: INT-REQ-003
def handler(event, context):
    response_string = _strip_code_fence(event["response_string"])
    response_object = json.loads(response_string)

    json_schema = event["json_schema"]
    validate(instance=response_object, schema=json_schema)

    return response_object
