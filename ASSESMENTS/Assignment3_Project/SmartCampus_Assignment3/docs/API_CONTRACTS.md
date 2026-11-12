# API contracts
All routes except health and facility catalogue require authentication unless otherwise stated.

## POST /api/bookings/
Request: `{ "facility": 1, "purpose": "AI lab session", "start_at": "2026-12-01T10:00:00+05:30", "end_at": "2026-12-01T11:00:00+05:30" }`
Success: booking object with status `REQUESTED`.
Conflict: HTTP 400 with overlap validation message. A PostgreSQL facility-row lock serializes requests for one facility.

## POST /api/bookings/{id}/transition/
Request: `{ "target": "APPROVED", "reason": "Academic session" }`
Only staff/manager/department approver may approve. Invalid transitions are rejected.

## POST /api/tickets/
Request: `{ "facility": 1, "title": "Projector issue", "description": "No display", "priority": "HIGH" }`
Success: ticket object with status `OPEN`.

## POST /api/tickets/{id}/transition/
Request: `{ "target": "ASSIGNED" }`
Technician/manager role required for operational transitions.

## POST /api/sensor-events/
Request: `{ "facility": 1, "event_id": "node-01-0001", "metric": "temperature", "value": 48.2, "observed_at": "2026-12-01T10:00:00Z" }`
Duplicate `event_id` is rejected by the unique database constraint. A temperature value >=45 creates a high-priority ticket.
