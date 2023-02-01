from db.django import get_portal_id

conf = {
    "BASE_URL":"https://telex.hu",
    "PORTAL_NAME": "Telex",
    "PORTAL_ID": get_portal_id("Telex")
}