def convert_to_dict(input_string:str) -> dict:
  parts = input_string.split(";")
  output_dict = {}
  for part in parts:
    key, value = part.split(":")
    output_dict[key.strip().lower()] = float(value.strip())
  return output_dict

