#!/usr/bin/env python3
from taxii2client.v21 import Server

server = Server(
    "http://127.0.0.1:5000/taxii2/",
    user="analyst",
    password="MeridianLab2026!",
)
api_root = server.api_roots[0]
print("API root title:", api_root.title)

collection = api_root.collections[0]
print("Collection:", collection.title, "-", collection.id)

bundle = collection.get_objects()
print("Objects retrieved:", len(bundle["objects"]))
for obj in bundle["objects"]:
    print(" -", obj["type"], obj["id"])
