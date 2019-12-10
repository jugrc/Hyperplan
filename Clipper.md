# CLIPPER

http://clipper.ai/

Clipper is a low-latency prediction serving system for machine learning.
The simplest way to start using Clipper is to use the Clipper Admin Python tool to start a local Clipper cluster using Docker.

## Model

1. Start a new Clipper cluster and deploy a Python function as your model from the Python shell 

`from clipper_admin import ClipperConnection, DockerContainerManager`

`clipper_conn = ClipperConnection(DockerContainerManager())`

2. Start Clipper (it may take a some time the first time)

`clipper_conn.start_clipper()`

> Output : 
19-12-10:19:20:19 INFO     [docker_container_manager.py:184] [default-cluster] Starting managed Redis instance in Docker
19-12-10:19:23:10 INFO     [docker_container_manager.py:276] [default-cluster] Metric Configuration Saved at /tmp/tmpZ3QViJ.yml
19-12-10:19:23:28 INFO     [clipper_admin.py:162] [default-cluster] Clipper is running

3. Register an application (here "hello-world"). This will create a prediction REST endpoint at http://localhost:1337/hello-world/predict

`clipper_conn.register_application(name="hello-world", input_type="doubles", default_output="-1.0", slo_micros=100000)`

> Output : 
19-12-10:19:23:28 INFO     [clipper_admin.py:236] [default-cluster] Application hello-world was successfully registered

4. Inspect Clipper to get all apps

`clipper_conn.get_all_apps()`

> Output : 
[u'hello-world']

5. Define a simple model that just returns the sum of each feature vector. Note that the prediction function takes a list of feature vectors as input and returns a list of strings.

```
def feature_sum(xs):
    return [str(sum(x)) for x in xs]
```

6. Import the python deployer package

`from clipper_admin.deployers import python as python_deployer`

7. Deploy the “feature_sum” function as a model. Notice that the application and model must have the same input type.

`python_deployer.deploy_python_closure(clipper_conn, name="sum-model", version=1, input_type="doubles", func=feature_sum)`

> Output : 
19-12-10:19:38:02 INFO     [deployer_utils.py:41] Saving function to /tmp/tmppDfdvIclipper
19-12-10:19:38:02 INFO     [deployer_utils.py:51] Serialized and supplied predict function
19-12-10:19:38:02 INFO     [python.py:192] Python closure saved
19-12-10:19:38:02 INFO     [python.py:198] Using Python 2 base image
19-12-10:19:38:02 INFO     [clipper_admin.py:534] [default-cluster] Building model Docker image with model data from /tmp/tmppDfdvIclipper
19-12-10:19:38:48 INFO     [clipper_admin.py:539] [default-cluster] Step 1/2 : FROM clipper/python-closure-container:0.4.1
19-12-10:19:38:48 INFO     [clipper_admin.py:539] [default-cluster]  ---> e9b89c285ef8
19-12-10:19:38:48 INFO     [clipper_admin.py:539] [default-cluster] Step 2/2 : COPY /tmp/tmppDfdvIclipper /model/
19-12-10:19:38:48 INFO     [clipper_admin.py:539] [default-cluster]  ---> 45a2f6b7a47e
19-12-10:19:38:48 INFO     [clipper_admin.py:539] [default-cluster] Successfully built 45a2f6b7a47e
19-12-10:19:38:48 INFO     [clipper_admin.py:539] [default-cluster] Successfully tagged default-cluster-sum-model:1
19-12-10:19:38:48 INFO     [clipper_admin.py:541] [default-cluster] Pushing model Docker image to default-cluster-sum-model:1
19-12-10:19:38:49 INFO     [docker_container_manager.py:409] [default-cluster] Found 0 replicas for sum-model:1. Adding 1
19-12-10:19:38:51 INFO     [clipper_admin.py:724] [default-cluster] Successfully registered model sum-model:1
19-12-10:19:38:51 INFO     [clipper_admin.py:642] [default-cluster] Done deploying model sum-model:1.

8. Tell Clipper to route requests for the “hello-world” application to the “sum-model”

`clipper_conn.link_model_to_app(app_name="hello-world", model_name="sum-model")`

> Output :
19-12-10:19:40:11 INFO     [clipper_admin.py:303] [default-cluster] Model sum-model is now linked to application hello-world

9. Your application is now ready to serve predictions

## Predictions

Now that you’ve deployed your model, you can start requesting predictions with a REST client at http://localhost:1337/hello-world/predict 

- With command line :
    `curl -X POST --header "Content-Type:application/json" -d '{"input": [1.1, 2.2, 3.3]}' 127.0.0.1:1337/hello-world/predict`

> Output : 
curl -X POST --header "Content-Type:application/json" -d '{"input": [1.1, 2.2, 3.3]}' 127.0.0.1:1337/hello-world/predict
{"query_id":2,"output":6.6,"default":false}

- With a Python interpreter : 
    ```
    import requests, json, numpy as np
    headers = {"Content-type": "application/json"}
    requests.post("http://localhost:1337/hello-world/predict", headers=headers, data=json.dumps({"input": list(np.random.random(10))})).json()
    ```

> Output : 
{u'default': False, u'output': 4.820642940849875, u'query_id': 1}

## Clean

If you close the Python interpreter, start a new one :

```
from clipper_admin import ClipperConnection, DockerContainerManager
clipper_conn = ClipperConnection(DockerContainerManager())
clipper_conn.connect()
```

`clipper_conn.stop_all()`

> Output : 
19-12-10:20:06:55 INFO     [clipper_admin.py:1424] [default-cluster] Stopped all Clipper cluster and all model containers