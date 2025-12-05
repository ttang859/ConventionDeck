# Project Idea: Card Convention App (ConventionDeck)

# Problem Description
- Difficult to find card shows in local area easily
    - requires searching across multiple sites and socials to find just one location
- Google Forms and payments are typically the way of vendors signing up for a convention
    - centralize it to one platform for all card shows
- Attendees are usually unsure about what vendors have what cards until you get to the show
    - time consuming for attendees to locate cards they want

# Project Description and High Level Outline
A centralized platform for card convention shows to be hosted, attended and organized.
- Vendors will be able to:
    - host their own card conventions on the site with a map of the convention
    - assign attending vendors to booths
    - upload and update their inventory before and during the card show
- Attendees will be able to:
    - view all card shows in their area
    - view which vendors are attending which conventions
    - view vendor inventory (add to cards of interest view)
    - pay for their attendance fee (transactional component)
- Both types of users:
    - have a QR code (and photo ID?) as their sign-in (host account has a QR scanner to check them in)

# Goals
- Accessibility and availability so services are always there for attendees and vendors to use
- Handle large amounts of attendees and vendors accessing site/app at once
- Secure and reliable transactions of payments

# Services and Descriptions
## user-service
- **Purpose:** Serve basic CRUD operations for user accounts.
- **Fields:**
  - `uid`
  - `email`
  - `user-type`
- **Communication:**
  - Sends an HTTP GET request to `convention-service:8000/health` to check availability.

---

## convention-service
- **Purpose:** Serve basic CRUD operations for conventions.
- **Fields:**
  - `cid`
  - `convention_name`
  - `host`
  - `location`
- **Communication:**
  - Performs HTTP GET `/health` checks to:
    - `booth-service`
    - `registration-service`
  - Pings the **Redis service** for health checks.

---

## registration-service
- **Purpose:** Serve basic CRUD operations for user registrations.
- **Fields:**
  - `rid`
  - `email`
  - `convention_name`
- **Notes:**
  - Both **attendees** and **vendors** can register for conventions.
  - Behavior may vary depending on `user-type`.
- **Communication:**
  - Pings the **Redis service** for health checks.

---

## booth-service
- **Purpose:** Serve basic CRUD operations for booth assignments.
- **Fields:**
  - `bid`
  - `convention_name`
  - `booth_num`
  - `vendor_id`
  - `payment_status`
- **Communication:**
  - Pings the **Redis service** for health checks.

---

## inventory-service
- **Purpose:** Serve basic CRUD operations for vendor inventory (possibly per convention).
- **Fields:**
  - `iid`
  - `vendor_id`
  - `item`
- **Communication:**
  - Pings the **Redis service** for health checks.

---

## user-db
- **Purpose:** isolated database for user information.
- **Role:** Holds user_id, email, username, and user_type

# Tech Stack
### Front-end:
- React.js
### Back-end:
<!-- - Spring Boot + Gradle (Java) -->
- FastAPI + Uvicorn
### Database: (still deciding)
<!-- - MongoDB (NoSQL)
- Supabase (build on Postgres SQL) -->
- Postgres Container (for now)
### NGINX
- Authentication
- Load Balancer
- API Gateway


