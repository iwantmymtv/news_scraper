from db.django import get_portal_id

conf = {
    "BASE_URL":"https://24.hu",
    "PORTAL_NAME": "24",
    "PORTAL_ID": get_portal_id("24")
}