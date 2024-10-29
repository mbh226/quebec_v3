## Information
#### Hypothesis Decorators
[Decorator Reference](https://www.lambdatest.com/blog/hypothesis-testing-in-python/#:~:text=Decorators%20in%20Hypothesis,-Before%20we%20proceed&text=Decorators%20are%20essentially%20functions%20themselves,or%20class%20with%20added%20functionality.)
- @given
	- turns a test function that accepts arguments into a randomized test
	- serves as main entry point to the Hypothesis
	- can be used to specify which arguments of a function should be parameterized over
		- can be positional or keyword arguments, but not both
	```
	#valid declarations of the @given decorator
	
	@given(integers(), integers())
	def a(x, y):
		pass
		
	@given(integers())
	def b(x, y):
		pass
		
	@given(y=integers())
	def c(x, y):
		pass

	@given(x=integers())
	def d(x,y)
		pass

	@given(x=integers(), y=integers())
	def e(x, **kwargs):
		pass
	
	@given(x=integers(), y=integers())
	def f(x, *args, *kwargs):
		pass

	class SomeTest(TestCase):
		@given(integers())
		def test_a_thing(self, x):
			pass
	
	```
- @example (NOT USED YET)
	- used in cases where we want to specify values we always want to be tested
	   <img width="563" alt="image" src="https://github.com/user-attachments/assets/2bc79d0e-098a-4be3-8690-d7ad121eca57">
    
		this test will always run for the input value _41_ along with other custom-generated test data by the Hypothesis _st.integers() function._

#### Hypothesis Strategies
[Strategies Reference](https://www.lambdatest.com/blog/hypothesis-testing-in-python/#:~:text=Decorators%20in%20Hypothesis,-Before%20we%20proceed&text=Decorators%20are%20essentially%20functions%20themselves,or%20class%20with%20added%20functionality.)
- the strategy method takes care of the process of generating this test data of the correct data type
- hypothesis offers a wide range of strategies such as integers, text, boolean, datetime, etc. For more complex scenarios, hypothesis also lets us set up composite strategies.

| STRATEGY               | DESCRIPTION                                                                 |
| ---------------------- | --------------------------------------------------------------------------- |
| _st.none()_            | Generates none values.                                                      |
| _st.booleans()_        | Generates boolean values (True or False).                                   |
| _st.integers()_        | Generates integer values.                                                   |
| _st.floats()_          | Generates floating-point values.                                            |
| _st.text()_            | Generates unicode text strings.                                             |
| _st.characters()_      | Generates single unicode characters.                                        |
| _st.lists()_           | Generates lists of elements.                                                |
| _st.tuples()_          | Generates tuples of elements.                                               |
| _st.dictionaries()_    | Generates dictionaries with specified keys and values.                      |
| _st.sets()_            | Generates sets of elements.                                                 |
| _st.binary()_          | Generates binary data.                                                      |
| _st.datetimes()_       | Generates datetime objects.                                                 |
| _st.timedeltas()_      | Generates timedelta objects.                                                |
| _st.one_of()_          | Choose one of the given strategies with equal probability.                  |
| _st.sampled_from()_    | Chooses values from a given sequence with equal probability.                |
| _st.lists()_           | Generates lists of elements.                                                |
| _st.dates()_           | Generates date objects.                                                     |
| _st.datetimes()_       | Generates datetime objects.                                                 |
| _st.just()_            | Generates a single value.                                                   |
| _st.from_regex()_      | Generates strings that match a given regular expression.                    |
| _st.uuids()_           | Generates UUID objects.                                                     |
| _st.complex_numbers()_ | Generates complex numbers.                                                  |
| _st.fractions()_       | Generates fraction objects.                                                 |
| _st.builds()_          | Builds objects using a provided constructor and strategy for each argument. |
| _st.characters()_      | Generates single unicode characters.                                        |
| _st.text()_            | Generates unicode text strings.                                             |
| _st.sampled_from()_    | Chooses values from a given sequence with equal probability.                |
| _st.data()_            | Generates arbitrary data values.                                            |
| _st.shared()_          | Generates values that are shared between different parts of a test.         |
| _st.recursive()_       | Generates recursively structured data.                                      |
| _st.deferred()_        | Generates data based on the outcome of other strategies.                    |
## Setup
#### Install
```
pip install hypothesis hypothesis_jsonschema pytest
```

#### Activate Environment
```
#i used my conda environment, but if you are using a python virtual environment you can use python -m venv

conda activate myenv
```

## Testing
A test in Hypothesis consists of two parts: 
1. A function that looks like a normal test in your test framework of choice but with some additional arguments
2. a @given decorator that specifies how to provide those arguments.

#### Test Scenario Creation
```python
#added a detailed, commented file called test_stock_hypothesis.py to JSON Validation directory to do some dynamic testing against our defined json schema

#NOTE: THIS IS COPY AND PASTED, FORMATTING COULD BE OFF

import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from hypothesis import given
from hypothesis import strategies as st
from hypothesis_jsonschema import from_schema

#load the JSON schema file
with open ('stock-schema.json') as stock_schema:
	schema = json.load(stock_schema)

#function to make sure that Hypotheis generated stocks are valid per schema

def validate_portfolio(portfolio):
	for stock in portfolio:
		validate(instance=stock, schema=schema)

#using @given indicates a test function should receive automatically generated input data

#if this test fails, we know theres an issue with how we're handling valid input
@given(from_schema(schema))
def test_valid_portfolio(portfolio):
#print whats being generated
	print(portfolio)
	validate(instance=portfolio, schema=schema)

#this is generating and testing invalid input

#st.lists is a hypothesis strategy used to generate lists

#st.one_of is a hypothesis strategy that lets you specify multiple strategies

@given(st.lists(st.one_of(
#this is going to generate valid stock entries based on schema
	from_schema(schema),
	#this is going to generate invalid stock entries that are zero or positive, which is invalid because schema indicates that a stock is an object, not an integer.
	st.integers(min_value=0),
	#this is going to generate dictionaries with random keys and integer values that have unexpected properties not allowed per the schema.
	st.dictionaries(
		#this is going to generate the dictionaries' keys
		keys=st.text(),
		#this is going to generate the dictionaries' values
		values=st.integers()
		)
	),
	#this makes sure the list generated has at least one element
	min_size=1
	)
)
#this function will validate a portfolio that has both valid and invalid entries and makes sure code can handle both
#it allows for failures in invalid entries and logs those failures without causing whole test to fail
#if this test fails, we know there's an issue with how invalid entries are processed.
def test_valid_invalid_portfolio(portfolio):
#validate valid stocks and iterate over each stock in portfolio
	for stock in portfolio:
	#checks that the stock is a dictionary, which is an object and then checks that the dictionary has ticker and nShares, which are required per the schema
		if isinstance(stock, dict) and 'ticker' in stock and 'nShares' in stock:
			try:
				validate(instance=stock, schema=schema)
			except ValidationError:
	
				print(f"{stock['ticker']} failed validation, moving to next stock.")

				continue
```

#### Run test
```
#I ran it it in verbose mode to get as much detail as I could
#I also used the -s flag so to disable output capturing so i could see the tested portfolios

pytest -v -s
```



#### Demo
- Passing test
	- leave everything as is
	- run pytest and everything should pass
	<img width="671" alt="image" src="https://github.com/user-attachments/assets/0ccca707-920c-44ba-83c0-663797ecdc9a">

- Failing test
	- Modified stock-schema.json to have a minLength of 6 instead of 4
	- Saved changes
	- Reran pytest -v -s
	<img width="666" alt="image" src="https://github.com/user-attachments/assets/86086f53-02f5-45e5-9055-930a5b0873de">

  - Failed because i defined a minimum size of 6 and a maximum size of 5 and minimum size cannot be greater than the maximum size.
	- Static testing doesn't detect logical inconsistencies and this is a runtime issue.
		- bandit -r test_stock_hypothesis.py results in no errors:
			<img width="651" alt="image" src="https://github.com/user-attachments/assets/1c517083-a906-4d4e-a51f-d4d180242053">

      - bandit -r stock-schema.json also results in no errors:
			  <img width="590" alt="image" src="https://github.com/user-attachments/assets/9540b03e-a50d-4039-ae0d-5bf76aaaeacf">



