from db.django import get_portal_id

conf = {
    "BASE_URL":"https://index.hu",
    "PORTAL_NAME": "Index",
    "PORTAL_ID": get_portal_id("Index")
}