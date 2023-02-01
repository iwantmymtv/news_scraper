from db.django import get_portal_id

conf = {
    "BASE_URL":"https://origo.hu",
    "PORTAL_NAME": "Origo",
    "PORTAL_ID": get_portal_id("Origo")
}