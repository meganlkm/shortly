# shortly

A simple URL shortening service.

## Setup

Install package and dependencies:

```bash
make setup
```

## Tests

Run the tests:

```bash
make test
```

## Deploy

Create apigateway, dynamodb table and lambda functions:

```bash
make build
make deploy
```

## Clean up

Delete AWS objects and local build

```bash
make clean
make reset
```
