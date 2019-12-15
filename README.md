# Clipper

http://clipper.ai/

- Un cluster Clipper est composé de plusieurs conteneurs Docker communiquant les uns avec les autres sur le réseau.
- L'outil Clipper Admin permet de communiquer avec ces conteneurs, d'en créer de nouveaux ou de détruire ceux qui existent.
- Une fois le cluster créé, on peut s'y connecter autant de fois qu'on veut.
- On peut créer et déployer des modèles simples (fonction simple qui prend une en entrée un vecteur ou une liste de vecteurs et qui retourne une prédiction ou une liste de prédictions sous forme de JSON ou d'une valeur) ou plus complexes (machine learning).
- L'un des objectifs de Clipper est de simplifier le déploiement et la maintenance des modèles de machine learning en production.
- 5 types d'entrée : int, float, double, byte, String.
- On peut enregistrer des applications avec le type d'entrée attendu, le temps latence maximal et la sortie par défaut si la prédiction n'est pas disponible. 
- Un seul cluster Clipper peut avoir plusieurs applications enregistrées et plusieurs modèles déployés en même temps.
- On doit lier une application à un modèle pour que Clipper route les requêtes reçues par l'API REST de l'application vers le modèle spécifié pour les prédictions.
- Un sytème de versioning est disponible, permettant d'améliorer un modèle sans supprimer les anciens.
- Clipper met en place une prédiction REST pour chaque application enregistrée dans Clipper. On peut interroger Clipper avec une ou plusieurs requêtes.
- Les requêtes sont des requêtes HTTP POST avec le header de type Content-type défini sur application/json et le corps sous la forme d'une chaîne de caractères JSON.
- Il aussi est possible de terminer tous les processus Clipper et de fermer les conteneurs Docker.

## Test d'une heuristique simple

On peut tester de 2 manières différentes Clipper : dans un Shell Python ou dans un script python.

L'exemple type de la documentation Clipper est la prédiction sur un modèle qui renvoie la somme de vecteurs : 

- On créé une instance de Clipper dans Docker.
- On enregistre une application *"hello-world"*.
- Ensuite on enregistre un modèle *"sum-model"* avec la fonction qui renvoie la somme d'une liste de vecteurs, puis on le déploie.
- On lie ensuite l'application avec le modèle (Clipper route les reuqêtes pour l'application ver le modèle), prête à servir les prédictions.
- Ensuite on fait une requête HTTP POST de la prédiction avec en entrée une liste de 10 nombres aléatoires entre 0 et 1.
- Enfin, on ferme tous les clusters Clipper et les conteneurs des modèles.


Voici l'output résultant de cet exemple :

```
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
```

## Différences avec Hyperplan

Voir ces différences va permettre à Antoine Sauray d'améliorer les fonctionnalités d'Hyperplan, car le logiciel est encore en Beta.

Tout d'abord, il faut créer un fichier Docker pour faire fonctionner Hyperplan alors que Clipper intègre directement dans son API des conteneurs Docker. Il faut donc plusieurs teminaux d'ouverts pour lancer Hyperplan (serveur, client) tandis qu'il en suffit d'un seul pour Clipper.

Cependant, l'interface d'Hyperplan est plus explicite que celle de Clipper, elle est à la fois simple et pratique. On peut facilement créer des fonctionnalités.

Clipper est un serveur en lui-même, il n'y a donc pas besoin d'un script python pour lancer un serveur. Pour faire fonctionner un programme avec Hyperplan il faut au moins 2 fichier, avec un serveur HTTP Flask. Cependant, on peut utiliser plusieurs algorithmes différents très facilement.

Hyperplan est aussi plus rapide que Clipper.

Hyperplan est donc plus dur d'utilisation, mais nous laisse plus libres dans nos choix grâce à son interface complète.