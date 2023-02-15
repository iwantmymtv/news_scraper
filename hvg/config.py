from db.django import get_portal_id

conf = {
    "BASE_URL":"https://hvg.hu",
    "PORTAL_NAME": "HVG",
    "PORTAL_ID": get_portal_id("HVG")
}