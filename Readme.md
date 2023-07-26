gradio app protected using okta authentication. Uses nginx as a reverse proxy along with vouch proxy as the auth handler.


the url given in the config files (my-service-3blf5p4gxa-nw.a.run.app) is that for the GCP cloud run instance of this service. To run this app locally, all instances of this URL must be replaced with localhost.


Secret and Id are passed through as env variable during running of container.
(when running locally , PORT must be specified , try 8080)
gcloud run deploy my-service \
--image gcr.io/thg-ml-dev/my-vouch-proxy \
--set-env-vars OAUTH_CLIENT_ID="clientID",OAUTH_CLIENT_SECRET="client secret" \
--platform managed \
--region europe-west2 \
--allow-unauthenticated


To add your own gradio app, create new python file in the models folder. In it, create a function which takes no argumemnts, and return a gradio blocks instance (follow the examples provided in the models folder). The app will automatically mount your app to its own endpoint, and create a link to your app in its homepage. 