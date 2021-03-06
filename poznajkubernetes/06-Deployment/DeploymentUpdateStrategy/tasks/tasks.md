# Korzystając z wiedzy na temat rolling update przetestuj:

## Działanie trybu Recreate
Do deploymentu wykorzystano plik [pkad-app.yaml](pkad-app.yaml):
```
$ k get deployments.apps 
NAME   READY   UP-TO-DATE   AVAILABLE   AGE
pkad   3/3     3            3           7m35s

$ k get rs
NAME              DESIRED   CURRENT   READY   AGE
pkad-596d856d5b   3         3         3       7m39s

$ k get pods
NAME                    READY   STATUS    RESTARTS   AGE
pkad-596d856d5b-2zxpr   1/1     Running   0          7m43s
pkad-596d856d5b-bpjfq   1/1     Running   0          7m43s
pkad-596d856d5b-lp5n7   1/1     Running   0          7m43s
```

Po wykonaniu deploymentu (została zaaktualizowana wersja tylko) widzimy, że odrazu wszystkie pody zmieniają status na terminating
```
$ k apply -f pkad-app.yaml 
deployment.apps/pkad configured

$ k get pods
NAME                    READY   STATUS        RESTARTS   AGE
pkad-596d856d5b-2zxpr   0/1     Terminating   0          9m46s
pkad-596d856d5b-bpjfq   0/1     Terminating   0          9m46s
pkad-596d856d5b-lp5n7   0/1     Terminating   0          9m46s

$ k get rs
NAME              DESIRED   CURRENT   READY   AGE
pkad-596d856d5b   0         0         0       9m59s
pkad-7bf9856857   3         3         3       5s

$ k get pod
NAME                    READY   STATUS    RESTARTS   AGE
pkad-7bf9856857-dnr57   1/1     Running   0          13s
pkad-7bf9856857-q56bv   1/1     Running   0          13s
pkad-7bf9856857-xdbv9   1/1     Running   0          13s
```

Po aktualizacji widzimy że faktucznie działa nowsza wersja:
```
$ k exec -it pkad-7bf9856857-dnr57 printenv | grep version
version=v2.0.0
```

## Szybki i wolny rolling update
Wolny deployment: [pkad-app-slow-update.yaml](pkad-app-slow-update.yaml)

```
$ k apply -f pkad-app-slow-update.yaml; k rollout status deployment pkad 
deployment.apps/pkad configured
Waiting for deployment "pkad" rollout to finish: 1 out of 3 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 1 out of 3 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 1 out of 3 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 2 out of 3 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 2 out of 3 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 2 out of 3 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 1 old replicas are pending termination...
Waiting for deployment "pkad" rollout to finish: 1 old replicas are pending termination...
deployment "pkad" successfully rolled out
```

Szybki deployment: [pkad-app-fast-update.yaml](pkad-app-fast-update.yaml)
```
k apply -f pkad-app-fast-update.yaml; k rollout status deployment pkad 
deployment.apps/pkad configured

Waiting for deployment "pkad" rollout to finish: 3 out of 10 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 3 out of 10 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 3 out of 10 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 3 out of 10 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 3 out of 10 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 4 out of 10 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 4 out of 10 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 5 out of 10 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 5 out of 10 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 5 out of 10 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 5 out of 10 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 5 out of 10 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 5 out of 10 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 6 out of 10 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 6 out of 10 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 6 out of 10 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 6 out of 10 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 7 out of 10 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 7 out of 10 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 7 out of 10 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 7 out of 10 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 8 out of 10 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 8 out of 10 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 8 out of 10 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 8 out of 10 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 9 out of 10 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 9 out of 10 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 9 out of 10 new replicas have been updated...
Waiting for deployment "pkad" rollout to finish: 2 old replicas are pending termination...
Waiting for deployment "pkad" rollout to finish: 2 old replicas are pending termination...
Waiting for deployment "pkad" rollout to finish: 2 old replicas are pending termination...
Waiting for deployment "pkad" rollout to finish: 1 old replicas are pending termination...
Waiting for deployment "pkad" rollout to finish: 1 old replicas are pending termination...
Waiting for deployment "pkad" rollout to finish: 1 old replicas are pending termination...
Waiting for deployment "pkad" rollout to finish: 9 of 10 updated replicas are available...
deployment "pkad" successfully rolled out
```

## Zmiany na deployment bez liveness i readiness
W sumie to wszysktie powyżej.

## Zmiany na deployment z działającym readiness
Przykład: [pkad-app-readiness.yaml](pkad-app-readiness.yaml)

## Zmiany na deployment z niedziałającym readiness (podaj np. błędny endpoint do sprawdzania)
Po zrobieniu deploymentu z poprzedniego przykładu gdzie(najpierw poprawnie), sutuacja wyglada jak poniżej:

```
NAME                    READY   STATUS    RESTARTS   AGE
pkad-756f9df6b-f7kbt    0/1     Running   0          68s
pkad-7967c4ff6f-2fblb   1/1     Running   0          3m25s
pkad-7967c4ff6f-tssd8   1/1     Running   0          3m11s
pkad-7967c4ff6f-vkf75   1/1     Running   0          3m38s

NAME              DESIRED   CURRENT   READY   AGE
pkad-5c6d757b95   1         1         0       70s
pkad-776d7fd9b6   3         3         3       2m23s
```

Deployemnt nie postępuje, po kilku minutach zakończyłem go ręcznie. Szczerze mówiąc to spodziewałem się że skoro mam ustawione parametry jak:
```
    timeoutSeconds: 1
    periodSeconds: 10
    failureThreshold: 3
```
To pod będzie "wstawał" i po ok 30 sekundach będzie "ubijany". 