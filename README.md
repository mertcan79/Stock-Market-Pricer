# Stock Market Pricer

A FastAPI based application which is capable of returning a list of daily close prices from the US stock market based on the input date range, ticker and requested currency.

## Date Parameters

The current JSON payload is not optimal.
It may not be immediately clear to clients what format the date range should be in, which could lead to errors.

It doesn't allow for flexibility in input. Clients may want to provide dates in a different format or time zone, which would not be possible with a fixed string format.

It may require extra parsing and validation on the server side to ensure that the string is formatted correctly and contains valid dates.

A better approach would be to follow a standardized date format, such as ISO 8601 format (YYYY-MM-DD), and accept the start and end dates as separate parameters. This would allow clients to provide dates in different formats or time zones, while also making it easier to validate and parse the input on the server side.

## Edge Cases

1. In case there is missing days in the requested date range, it is filled with the price from the previous day.
2. In case the starting day in the requested date range is missing, it is filled with 0. It can be filled with the previous day as well but it is currently not implemented.
3. The last 31 days are shown if the date range field is empty.
4. Current FX API returns the rates in a descending date order, if this changes in the future calculations will be wrong.
5. In case of wrong currency or ticker, users should be made aware about the wrong input. Currently it is not implemented. HTTPException can be used.

## Running the project

The app can be run from the command line using `python main.py`

## Testing

A test script is included where daily stock price is requested in a different currency than USD using different date formats.

## Notes

API keys normally should not be public and env. variables should be used. 
Some things are left on a non production level ready state for simplicity and explicity rather than creating a production ready project. Thus, Docker is not included.