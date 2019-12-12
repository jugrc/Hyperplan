from clipper_admin import ClipperConnection, DockerContainerManager
from clipper_admin.deployers import python as python_deployer
import requests, json, datetime, time, numpy as np

# Model to predict
def feature_sum(xs):
    return [str(sum(x)) for x in xs]

def predict(addr, app, x, batch = False):
    # Address where requesting predictions with a REST client
    url = "http://%s/%s/predict" % (addr, app)

    # Input (vector or list of vector) type: [double] | [int] | [string] | [byte] | [float]
    if batch:
        req_json = json.dumps({'input_batch': x})
    else:
        req_json = json.dumps({'input': list(x)})

    headers = {'Content-type': 'application/json'}
    start = datetime.datetime.now()

    # Requesting with REST client at the previous url
    r = requests.post(url, headers = headers, data = req_json)

    end = datetime.datetime.now()
    latency = (end - start).total_seconds() * 1000.0
    print("'%s', %f ms" % (r.text, latency))

if __name__ == "__main__":
    # Define the app's name and the model's name
    app = "hello-world"
    model = "sum-model"
    
    # Start a new Clipper cluster connecting to a Docker container
    clipper_conn = ClipperConnection(DockerContainerManager())
    clipper_conn.start_clipper()

    # Register an application
    clipper_conn.register_application(name = app, input_type = "doubles", default_output = "-1.0", slo_micros = 100000)

    # Inspect Clipper to get all apps
    clipper_conn.get_all_apps()

    # Deploy the "feature_sum" function as a model. Notice that the application and model must have the same input type.
    python_deployer.deploy_python_closure(clipper_conn, name = model, version = 1, input_type = "doubles", func = feature_sum)

    # Tell Clipper to route requests for the "hello-world" application to the "sum-model"
    clipper_conn.link_model_to_app(app_name = app, model_name = model)

    # To avoid error "No connected models found for query"
    # Wait 10s in order to let the model go on clipper
    time.sleep(10)

    # Predict on a 10 random doubles list between 0 and 1
    predict("localhost:1337", app, np.random.random(10))

    # Stop all Clipper docker containers
    clipper_conn.stop_all()