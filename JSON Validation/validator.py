import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError

#load the stock file
with open ('stock.json') as stock_file:
    portfolio = json.load(stock_file)

#load the scheme file
with open ('stock-schema.json') as stock_schema:
    schema = json.load(stock_schema)

#setting to true for validation success
all_valid = True

for stock in portfolio:
    try:
        validate(instance=portfolio, schema=schema)
    except ValidationError as e:
        all_valid = False
        print("Validation of stock file failed!")
        print(f"{e.message}")
        break

if all_valid:
    print("Portfolio validated successfully.")
else:
    print("One or more stocks in portfolio failed validation.")