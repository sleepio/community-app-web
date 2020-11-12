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
1. Changes made to the frontend will NOT be detected automatically, yet. You can run `docker-compose exec community_app_web npx gulp watch` to trigger the watcher. How well this works is unknown but check out the `gulpfile.js` in the `frontend` directory to see details.

## Test

### Python/Django
1. Run `docker-compose up --build community_app_web-test` to run the pytest suite locally.

### Javascript
Testing setup not present yet for frontend JS code. Misago claims to provide a [suite of Mocha.js tests](https://github.com/rafalp/Misago#frontend), but the gulp task to run it is not present in their gulpfile.
