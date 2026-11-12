# Smart Campus Facility Booking & Maintenance Platform
**CSA10 Software Engineering – Assignment 3 (CO3)**  
Student: Doma Saketh | Register No: 192525018

## Stack
- Frontend: Vue 3 + TypeScript + Vite
- Backend: Django REST Framework
- Database: PostgreSQL 16
- Containerization: Docker Compose

## Run with Docker
1. Install Docker Desktop and start the Docker engine.
2. Copy `.env.example` to `.env` and replace both secrets.
3. Run:
   ```bash
   docker compose up --build -d
   docker compose exec backend python manage.py makemigrations campus
   docker compose exec backend python manage.py migrate
   docker compose exec backend python manage.py seed_demo
   ```
4. Open `http://localhost:8080` (frontend), `http://localhost:8000/api/health/` (API).
5. Demo accounts: `student / CampusDemo123!` and `manager / ManagerDemo123! and technician / TechDemo123!`. Development only; change passwords and secret keys before deployment.

## Run locally without Docker
Backend:
```bash
cd backend
python -m venv .venv
# activate the environment
pip install -r requirements.txt
# Configure PostgreSQL environment variables, then:
python manage.py makemigrations campus
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```
Frontend:
```bash
cd frontend
npm install
npm run dev
```
Set `VITE_API_URL=http://localhost:8000/api` if needed.

## API routes
- `GET /api/health/`
- `GET /api/facilities/`
- `GET, POST /api/bookings/`
- `POST /api/bookings/{id}/transition/` with target
- `GET, POST /api/tickets/`
- `POST /api/tickets/{id}/transition/`
- `GET, POST /api/sensor-events/` (technician/manager)
- `GET /api/audit/` (manager/admin)

HTTP Basic authentication is enabled for this academic prototype. The browser sends credentials over the API; use HTTPS and preferably session/OIDC authentication for deployment.

## Booking lifecycle
REQUESTED → APPROVED → CONFIRMED → IN_USE → COMPLETED  
REQUESTED / APPROVED / CONFIRMED → CANCELLED

## Maintenance lifecycle
OPEN → ASSIGNED → IN_PROGRESS → RESOLVED → CLOSED

## Git workflow evidence exercise (perform in your own GitHub account)
```bash
git init
git add .
git commit -m "chore: scaffold smart campus platform"
git switch -c feature/booking-overlap
# implement or adjust booking overlap behaviour
git add backend/campus/services.py
git commit -m "feat: reject overlapping facility bookings"
git switch main
git switch -c feature/ticket-sla
# add ticket SLA/report behaviour
git add backend/campus
git commit -m "feat: add maintenance ticket workflow"
git switch main
git merge --no-ff feature/booking-overlap
git merge --no-ff feature/ticket-sla
git tag -a v1.0.0 -m "Assignment 3 release"
```
To demonstrate conflict resolution transparently, create two separate branches that edit the same policy line, merge one, then merge the second and resolve the conflict manually. Record the actual conflict and resolution in the report. Do not fabricate commit hashes or pretend a merge occurred when it did not.

## Tests and limitations
Run:
```bash
docker compose exec backend python manage.py test campus
```
Tests cover booking creation, overlap rejection and invalid state transition. A real simultaneous-request test using PostgreSQL transactions, sensor alert integration, SLA escalation, deployment restart/persistence, security and load tests remain required before production. The assignment scenario's 300-user peak is a target for a bounded experiment, not a claim of measured capacity.
