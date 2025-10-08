def test_hello(client):
    response = client.get("/api/hello")
    assert response.json() == "Hello"


def test_ping_pong(client):
    response = client.get("/api/ping")
    actual = []
    for res in response.iter_lines():
        print(res)

        actual.append(res)
    assert "ping" in actual[0]
    assert "pong" in actual[0]
