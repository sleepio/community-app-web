# Community App Web, Powered by [Misago](https://github.com/rafalp/Misago)

## Run locally
1. Run the rest of the BH local development suite with [`bhspin up`](https://github.com/sleepio/ops-tools/blob/root/README.md#6-up-the-backend).
1. Run `docker-compose up --build community_app_web`.
1. Hit up the local server [here](localhost:8200).


## Development

### Python/Django
1. Run the local server by following the instructions above.
1. Changes made to Python code will be detected and the server will refresh automatically.

### Javascript
1. Run the local server by following the instructions above.
1. Changes made to the frontend will NOT be detected automatically.

## Test

### Python/Django
1. Run `docker-compose up --build community_app_web-test` to run the pytest suite locally.

### Javascript
Testing setup not present yet for frontend JS code.
