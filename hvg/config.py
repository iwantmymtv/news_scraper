from db.django import get_portal_id

conf = {
    "BASE_URL":"https://hvg.hu",
    "PORTAL_NAME": "Hvg",
    "PORTAL_ID": get_portal_id("Hvg")
}