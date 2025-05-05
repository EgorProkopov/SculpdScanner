import requests

url = "http://localhost:7777/generate_scanner_description"

image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/PNG_transparency_demonstration_1.png/640px-PNG_transparency_demonstration_1.png"

user_info_json = {
  "email": "newuser@example.com",
  "image": "http://example.com/image3.jpg",
  "name": "New User",
  "gender": "male",
  "birthday": "1985-05-15T00:00:00Z",
  "height": 180.5,
  "height_type": "cm",
  "weight": 82.0,
  "weight_type": "kg",
  "fitness_level": "intermediate",
  "improve_body_parts": ["abs", "shoulders", "chest"],
  "exercise_limitations": ["no_overhead_pressing"],
  "nutrition_goal": "lose_weight",
  "equipment_list": ["cable_machine", "barbell", "platform", "barbell", "ez_bar"],
  "training_days": 4,
  "workout_time": 60
}

payload = {
    "user_info": user_info_json,
    "image_url": image_url
}

resp = requests.post(url, json=payload)
print("Status code:", resp.status_code)
print("Content-Type:", resp.headers.get("Content-Type"))
print("Body text:", repr(resp.text))
