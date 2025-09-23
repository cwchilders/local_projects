
def format_details(data):
  price = f"**{data.get('price', 'N/A')}**"
  other_data = []
  for key, value in data.items():
    if key not in ['price', 'address']:
      if key == 'beds' and value == '1':
        key = 'bed'
      elif key == 'baths' and value == '1':
        key = 'bath'
      other_data.append(f"{value} {key}")
  return f"{price} {' '.join(other_data)}"

# Example usage:
data = {'price': '$240,000', 'address': '1186 Highway 554,\xa0El Rito, NM 87530', 'beds': '1', 'baths': '1', 'sqft': '1,124'}
print(parse_data(data))
