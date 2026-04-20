## Plan: DRF Backend for Property Booking Flow

TL;DR: Build a new Django app with DRF models, serializers, and API views for property listings, property detail, account status, contact flow, email-based auth, and premium access/payment state. Keep the frontend out of scope and provide clean API endpoints matching the requested page logic.

**Steps**
1. Create a new app, e.g. `listings`, and register it in `dnd_backend/settings.py`.
2. Install/enable Django REST Framework and configure it in `INSTALLED_APPS`.
3. Define models in `listings/models.py`:
   - `Property` with fields: `name`, `city`, `side`, `description`, `order_number`, `short_term_rate`, `long_term_rate`, `type`, `gps_lat`, `gps_lng`, `bedrooms`, `ac`, `internet`, `hot_water`, `parking`, `pool`, `roof_access`, `balcony`, `washing_machine`, `whatsapp`, `availability_months` or related `PropertyAvailability`.
   - `PremiumAccess` or extend `User` via `Profile` to store `is_paid`, `premium_until`, and `stripe_payment_id`.
   - `EmailVerificationCode` for the email sign-in/signup flow.
4. Implement serializers in `listings/serializers.py`:
   - `PropertyListSerializer` with computed `display_rate` based on selected period and availability filters.
   - `PropertyDetailSerializer` with all requested fields and boolean yes/no conversions.
   - `AccountSerializer` returning email/premium status and expiry text.
5. Implement DRF views / viewsets in `listings/views.py`:
   - `PropertyListView` with query params `city`, `availability`, `period`, ordered by `order_number`, paginated 18 per page.
   - `PropertyDetailView` returning single-property details by id or slug.
   - `ContactOwnerFlowView` returning the current step state based on auth/payment and whether property contact is allowed.
   - `AccountView` returning logged-in user email, premium expiry, and available actions.
6. Add auth endpoints:
   - `POST /api/auth/email-start/` to submit email and create/send code.
   - `POST /api/auth/email-verify/` to verify code and log in/register the user.
   - `POST /api/auth/logout/` to log out.
   - Use session auth or token auth; DRF session auth is acceptable for API-only flows.
7. Add payment endpoints and premium state handling:
   - `POST /api/payments/create-session/` or `POST /api/payments/activate/` to record premium access.
   - Save `premium_until = now + 24 hours` on successful payment.
   - Expose `is_premium` and `premium_until` to API clients.
8. Wire URLs in `dnd_backend/urls.py` with `include('listings.urls')` and admin.
9. Add pagination class for page numbers and response shape matching page listing requirements.
10. Document the endpoints and expected API contract.

**Verification**
1. Confirm `manage.py runserver` starts after adding the app and DRF.
2. Use Django shell or API client to create a property and verify `GET /api/properties/` returns sorted 18-per-page listings.
3. Verify `GET /api/properties/{id}/` returns all requested detail fields and contact link state.
4. Test auth flow: email submit, code verify, logged-in account response.
5. Test premium state: create premium payment record, verify `AccountView` returns `ACCESS GRANTED` and `premium_until`.

**Decisions / assumptions**
- Build backend-only JSON API endpoints; no frontend templates in this phase.
- Implement email/code auth first; social login is deferred.
- Stripe integration can be added as a real checkout flow later; initial plan includes payment status fields and activation endpoints.
- Property availability months are stored and exposed in a computed month-year list.
