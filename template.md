Add an endpoint to satisfy next requirements:

- Endpoint: "GET /api/atm/checkout"
- Query params: plate (string) and cajeroKey (string uuid)
- Response: 
    ```json
    { "tx": "uuid", "amount": 3500, "stayMinutes": 120 }
    ```
    Return a random tx

____________________________

Add an endpoint to satisfy next requirements:
- Endpoint: "GET /api/atm/gracePeriod"
- Query params: plate (string) and cajeroKey (string uuid)
- Response: 
    ```json
    { "hasGracePeriod": true, "minutesRemaining": 15 }
    ```
____________________________

Update the endpoint:
- Endpoint: "POST /api/atm/charge"
- Request body: 
    ```json
    { "tx": "uuid", "status": "ATM-OK", "mode": "electronic", "lines": [1]}
    ```