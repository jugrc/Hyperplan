# CLIPPER

http://clipper.ai/

Il y a 2 manières de lancer un cluster Clipper. En ligne de commandes dans le shell python ou via un script. 
Ici, nous allons plutôt utiliser des scripts.

## Conditions requises pour faire fonctionner Clipper

Avoir Python 2, 3.5, 3.6, ou 3.7.

Lancer dans un terminal la commande `pip install clipper_admin`.

### basicQuerySimplified

J'ai adapté le code d'un exemple de Clipper pour une requête basique avec le client.
Le code est commenté si vous voulez plus de précision.

Pour lancer le script taper la commande `python basicQuerySimplified.py`.

- Ce script très simple se connecte à Clipper et créé une application *"hello-world"* qui prend en entrée des doubles.
- Ensuite, on déploie un modèle nommé *"sum-model"* qui utilise une fonction qui retourne la somme d'une liste de vecteurs doubles.
- Ensuite on lie le modèle à l'application, puis se lance la fonction *predict()*.
- Cette fonction demande des prédictions avec un client REST à l'adresse *http://localhost:1337/hello-world/predict*.
- Ici, la prédiction renvoie la somme de 10 vecteurs doubles aléatoirement tirés entre 0 et 1.
- Enfin, on ferme tous les cluster Clipper et les conteneurs Docker.

> Output :
19-12-12:18:22:59 INFO     [docker_container_manager.py:184] [default-cluster] Starting managed Redis instance in Docker
19-12-12:18:23:02 INFO     [docker_container_manager.py:276] [default-cluster] Metric Configuration Saved at /tmp/tmpQnjLyk.yml
19-12-12:18:23:03 INFO     [clipper_admin.py:162] [default-cluster] Clipper is running
19-12-12:18:23:03 INFO     [clipper_admin.py:236] [default-cluster] Application hello-world was successfully registered
19-12-12:18:23:03 INFO     [deployer_utils.py:41] Saving function to /tmp/tmpmhqDlaclipper
19-12-12:18:23:03 INFO     [deployer_utils.py:51] Serialized and supplied predict function
19-12-12:18:23:03 INFO     [python.py:192] Python closure saved
19-12-12:18:23:03 INFO     [python.py:198] Using Python 2 base image
19-12-12:18:23:03 INFO     [clipper_admin.py:534] [default-cluster] Building model Docker image with model data from /tmp/tmpmhqDlaclipper
19-12-12:18:23:03 INFO     [clipper_admin.py:539] [default-cluster] Step 1/2 : FROM clipper/python-closure-container:0.4.1
19-12-12:18:23:03 INFO     [clipper_admin.py:539] [default-cluster]  ---> e9b89c285ef8
19-12-12:18:23:03 INFO     [clipper_admin.py:539] [default-cluster] Step 2/2 : COPY /tmp/tmpmhqDlaclipper /model/
19-12-12:18:23:03 INFO     [clipper_admin.py:539] [default-cluster]  ---> 1b1aa3a2925a
19-12-12:18:23:03 INFO     [clipper_admin.py:539] [default-cluster] Successfully built 1b1aa3a2925a
19-12-12:18:23:03 INFO     [clipper_admin.py:539] [default-cluster] Successfully tagged default-cluster-sum-model:1
19-12-12:18:23:03 INFO     [clipper_admin.py:541] [default-cluster] Pushing model Docker image to default-cluster-sum-model:1
19-12-12:18:23:04 INFO     [docker_container_manager.py:409] [default-cluster] Found 0 replicas for sum-model:1. Adding 1
19-12-12:18:23:05 INFO     [clipper_admin.py:724] [default-cluster] Successfully registered model sum-model:1
19-12-12:18:23:05 INFO     [clipper_admin.py:642] [default-cluster] Done deploying model sum-model:1.
19-12-12:18:23:05 INFO     [clipper_admin.py:303] [default-cluster] Model sum-model is now linked to application hello-world
'{"query_id":0,"output":4.295446139258758,"default":false}', 4.292000 ms
19-12-12:18:23:57 INFO     [clipper_admin.py:1424] [default-cluster] Stopped all Clipper cluster and all model containers

### basicQuery

Cet exemple est le script présent sur le git Clipper.

Pour lancer le script taper la commande `python basicQuery.py`.

C'est une version améliorée du précédent programme.

- Il y a une boucle infinie qui utilise la fonction *predict()* continuellement sur une liste de 200 vecteurs doubles aléatoirement tirés entre 0 et 1.
- Pour quitter cette boucle, le client doit taper dans le terminal ctrl-C. 

## Fermer les cluster Clipper et les conteneurs

S'il y a un problème dans un des scripts et que la commande qui ferme Clipper ne s'est pas exécutée, il est important de fermer Clipper et ses conteneurs pour lancer à nouveau un script.

Pour ce faire, lancer `python closeClipper.py` afin de s'assurer que les conteneurs Docker du modèle et les cluster de Clipper se ferment.