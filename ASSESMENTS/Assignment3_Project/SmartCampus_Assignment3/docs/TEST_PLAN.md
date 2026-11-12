# Validation plan
| ID | Scenario | Expected result | Current evidence |
|---|---|---|---|
| B01 | Valid facility booking | REQUESTED record persists | Django test defined |
| B02 | Overlapping booking | Request rejected; no second booking | Django test defined |
| B03 | Invalid state transition | HTTP/service validation error | Django test defined |
| B04 | Student attempts approval | 403 permission denial | Service permission rule defined |
| M01 | Sensor temperature >=45 | High priority ticket created | View logic implemented; integration test required |
| M02 | Duplicate sensor event ID | Unique constraint rejects duplicate | Database constraint defined |
| D01 | Restart backend container | Database data persists | Requires local Docker execution |
| D02 | Rebuild clean deployment | Frontend/API available | Requires local Docker execution |
| C01 | Two simultaneous booking requests | One overlapping request rejected | PostgreSQL concurrency test required |
| L01 | 300 concurrent users | Report measured throughput and errors | Not executed; do not claim capacity |
