# GoSave

A full-stack price monitoring platform that lets users track product prices across online stores. The backend handles user authentication, item tracking, and notifications, while background workers automatically scrape and compare prices on a daily schedule.

## Features

- User-based item price tracking and monitoring
- Automated price scraping via async background jobs
- Real-time notifications on price changes
- Low-latency REST API for user-facing endpoints

## Tech Stack

- **Language:** Python
- **Backend:** FastAPI
- **Task Queue:** Celery
- **Database:** MongoDB
- **Frontend:** React
