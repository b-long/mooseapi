import json

from fastapi.testclient import TestClient

from mooseapi.main import app

client = TestClient(app)

input = {
    "foo": "bar",
    "baz": ["bizz", "buzz", "bozz"],
    "meaning-of-life": 42,
}

expected_output = {
    "keys": ["foo", "baz", "meaning-of-life"],
    "values": ["bar", ["bizz", "buzz", "bozz"], 42],
}


def test_post_arbitrary_typed_body():
    body = json.dumps(input)
    response = client.post("/typed-arbitrary-data", data=body)

    assert response.status_code == 200
    assert response.json() == expected_output


def test_post_arbitrary_body():
    body = json.dumps(input)
    response = client.post("/arbitrary-data", data=body)

    assert response.status_code == 200
    assert response.json() == expected_output
