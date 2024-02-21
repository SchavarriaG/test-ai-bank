import app
import json

with open("evento.json") as f:
  raw_data = f.read()
evento = json.loads(raw_data.encode("utf-8-sig"))

context = "nulo"
try:
    app.lambda_handler(evento, context)
except Exception as e:
    raise e
