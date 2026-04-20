# API Examples for Property Booking Backend

## Media File Handling

- **Images**: Up to 10 images per property (image_1 through image_10)
  - Supported formats: JPEG, PNG, GIF, WebP (via Pillow)
  - Stored in `media/properties/images/`
  - URLs returned in API responses

- **Videos**: Up to 3 videos per property (video_1 through video_3)
  - Supported formats: MP4, AVI, MOV, MKV
  - Stored in `media/properties/videos/`
  - URLs returned in API responses

**Note**: Media files are uploaded via Django admin or direct API endpoints. Frontend should handle file uploads to the appropriate property fields.

## Auth Flow

### 1. Start email registration

`POST /api/auth/email-start/`

Request body:
```json
{
  "email": "user@example.com",
  "password": "mypassword123"
}
```

Response example:
```json
{
  "detail": "Verification code sent to email.",
  "code": "123456"
}
```

### 2. Verify email code to activate account

`POST /api/auth/email-verify/`

Request body:
```json
{
  "email": "user@example.com",
  "code": "123456"
}
```

Response example:
```json
{
  "detail": "Account activated successfully."
}
```

### 3. Login with email and password

`POST /api/auth/login/`

Request body:
```json
{
  "email": "user@example.com",
  "password": "mypassword123"
}
```

Response example:
```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "",
    "last_name": "",
    "is_premium": false,
    "premium_until": null
  }
}
```

### 4. Refresh the access token

`POST /api/auth/token/refresh/`

Request body:
```json
{
  "refresh": "<refresh_token>"
}
```

Response example:
```json
{
  "access": "<new_access_token>"
}
```

### 4. Account status

`GET /api/account/`

Header:
```
Authorization: Bearer <access_token>
```

Response example:
```json
{
  "email": "user@example.com",
  "is_premium": false,
  "premium_until": null,
  "status_message": "GET ACCESS"
}
```

### 5. Activate premium access (payment stub)

`POST /api/account/premium/`

Header:
```
Authorization: Bearer <access_token>
```

Request body:
```json
{
  "payment_id": "stripe_session_123"
}
```

Response example:
```json
{
  "detail": "Premium access activated for 24 hours.",
  "premium_until": "2026-04-17T14:34:00Z",
  "is_premium": true
}
```

### 6. Contact owner status

`GET /api/account/contact-owner/`

Header:
```
Authorization: Bearer <access_token>
```

Response examples:
- not logged in or account not activated:
```json
{
  "step": 1,
  "title": "Log in or sign up",
  "action": "login"
}
```
- logged in, account activated, unpaid:
```json
{
  "step": 2,
  "title": "Get full access to all landlords direct Whatsapp chats",
  "action": "purchase"
}
```
- logged in, account activated, premium:
```json
{
  "step": 3,
  "title": "Whatsapp to the property owner directly",
  "action": "whatsapp"
}
```

## Property Listing

### 1. List properties

`GET /api/properties/?city=Flic En Flac&availability=May 2026&period=Short-Term&page=1`

Response example (paginated):
```json
{
  "count": 42,
  "next": "http://localhost:8000/api/properties/?page=2...",
  "previous": null,
  "results": [
    {
      "id": 1,
      "PropertyName": "Beachfront Apartment",
      "PropertyCity": "Flic En Flac",
      "PropertySide": "West",
      "PropertyRatePerDay": "80.00",
      "PropertyRatePerMonth": "1500.00",
      "PropertyRate": "$80.00/day",
      "PropertyOrderNumber": 1
    }
  ]
}
```

### 2. Property detail

`GET /api/properties/1/`

Response example:
```json
{
  "propertyID": 1,
  "propertyName": "Beachfront Apartment",
  "propertyCity": "Flic En Flac",
  "propertySide": "West",
  "propertyDescription": "A sunny apartment near the beach.",
  "propertyAvailability": ["May 2026", "June 2026"],
  "propertyRateShortTerm": "$80.00/day",
  "propertyRateLongTerm": "$1500.00/month",
  "propertyType": "Appartment",
  "propertyGPS": "-20.512357,57.497616",
  "propertyBedrooms": 2,
  "propertyAC": "yes",
  "propertyInternet": "yes",
  "propertyHotWater": "yes",
  "propertyParking": "yes",
  "propertyPool": "no",
  "propertyRoofAccess": "no",
  "propertyBalcony": "yes",
  "propertyWashingMachine": "yes",
  "propertyWhatsapp": "+23012345678",
  "propertyImages": [
    {
      "id": 1,
      "url": "http://localhost:8000/media/properties/images/property_1_image_1.jpg",
      "name": "property_1_image_1.jpg"
    },
    {
      "id": 2,
      "url": "http://localhost:8000/media/properties/images/property_1_image_2.jpg",
      "name": "property_1_image_2.jpg"
    }
  ],
  "propertyVideos": [
    {
      "id": 1,
      "url": "http://localhost:8000/media/properties/videos/property_1_video_1.mp4",
      "name": "property_1_video_1.mp4"
    }
  ],
  "contactStatus": "login_required",
  "contactUrl": null
}
```

If the user has premium access, `contactUrl` will return a WhatsApp link:
```json
"contactUrl": "https://wa.me/23012345678"
```
