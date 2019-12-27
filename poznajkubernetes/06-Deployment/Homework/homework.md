# Skoro wiesz jak działa ReplicaSet i Deployment:

## Stwórz Deployment dla Podów które w poprzednim module Twoje serwisy udostępniały
Wykorzystano [my-app.yaml](my-app.yaml)

## Spróbuj to zrobić deklaratywnie i imperatywnie – Deployment jak i Serwis
W sumie to zrobiłem tylko deklaratywnie

## Zeskaluj aplikację do 3 replik
```
$ k scale deployment homework-app --replicas=3 
deployment.apps/homework-app scaled

$ k get pods
NAME                            READY   STATUS    RESTARTS   AGE
homework-app-867fbcf6b5-b2lxv   1/1     Running   0          4m18s
homework-app-867fbcf6b5-c6hcf   1/1     Running   0          4m5s
homework-app-867fbcf6b5-x5hlr   1/1     Running   0          6m10s
```

## Zeskaluj aplikację do 1 repliki jeżeli aktualnie ma ona 3 działające repliki

```
$ k scale deployment homework-app --replicas=1
deployment.apps/homework-app scaled
[jarek@master-node:Homework (⎈|kubernetes-admin@kubernetes:default)]
$ k get pods
NAME                            READY   STATUS        RESTARTS   AGE
homework-app-867fbcf6b5-b2lxv   0/1     Terminating   0          4m50s
homework-app-867fbcf6b5-c6hcf   0/1     Terminating   0          4m37s
homework-app-867fbcf6b5-x5hlr   1/1     Running       0          6m42s
```

## Wyciągnij historię pierwszego deploymentu
```
$ k rollout history deployment homework-app --revision=1
deployment.apps/homework-app with revision #1
Pod Template:
  Labels:	app=homework-app
	pod-template-hash=867fbcf6b5
  Init Containers:
   busybox:
    Image:	busybox
    Port:	<none>
    Host Port:	<none>
    Command:
      sh
      -c
      echo "<h1>Czołem!</h1>" > /storage/index.html;
    Environment:	<none>
    Mounts:
      /storage/ from storage-volume (rw)
  Containers:
   homework-app:
    Image:	nginx
    Port:	80/TCP
    Host Port:	0/TCP
    Environment:
      version:	v1
      pod:	 (v1:metadata.name)
    Mounts:
      /usr/share/nginx/html from storage-volume (rw)
  Volumes:
   storage-volume:
    Type:	EmptyDir (a temporary directory that shares a pod's lifetime)
    Medium:	
    SizeLimit:	<unset>
```

## Zweryfikuj, że deployment się udał
```
$ k rollout status deployment homework-app 
deployment "homework-app" successfully rolled out
```

## Zastanów się ile dodatkowych sekund potrzebuje Twoja aplikacja by poprawnie wystartować
Akurat w tym przypadku najwiecej trwa pierwszy deployment, gdyż trzeba wykonac initContainera, a dalsze deploymenty odbywają sie już w ekspresowym tempie.
