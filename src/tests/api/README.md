## Integration Test

The following tests are to be run to ensure that changes to the any part 
of the codebase doesn't break the API. One way things can break is if the schema
of either Library, Chunk or Document changes. It is important to ensure that we
are returning data that is consistent across any iteration.

### To Test

It is recommended to start a fresh database instance to run the tests or else you'll
encounter several fail cases. Simply launch a new docker container from the `/src/` directory:

```bash
docker build -t vector-db-image:latest .
# Use a different port other than 8000 if you're already running 1 instance on that port
docker run --name vector-db -p 8001:8000 vector-db-image:latest 
```

Ensure that you have the following env var in your env file in the `/src/` directory

```
# Use the right port number where you launch your test db container
PYTEST_DB_URI=http://localhost:8001 
```

To run the test simply run:
```bash
poetry run pytest
```