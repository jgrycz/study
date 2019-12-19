# Przetestuj każde z pytań w praktyce!


## Co się stanie kiedy dodasz Pod spełniający selektor ReplicaSet?
RS została stworzona na podstawie [replica-set.yaml](replica-set.yaml)

Wszystko chodzi elegancko:
```
NAME            READY   STATUS    RESTARTS   AGE
test-rs-654rx   1/1     Running   0          71s
test-rs-z2qv7   1/1     Running   0          71s

$ k describe rs test-rs 
Name:         test-rs
Namespace:    default
Selector:     tier=test-rs
Labels:       app=demo-rs
              tier=test-rs
Annotations:  kubectl.kubernetes.io/last-applied-configuration:
                {"apiVersion":"apps/v1","kind":"ReplicaSet","metadata":{"annotations":{},"labels":{"app":"demo-rs","tier":"test-rs"},"name":"test-rs","nam...
Replicas:     2 current / 2 desired
Pods Status:  2 Running / 0 Waiting / 0 Succeeded / 0 Failed
Pod Template:
  Labels:  tier=test-rs
  Containers:
   pkad:
    Image:        poznajkubernetes/pkad:green
    Port:         <none>
    Host Port:    <none>
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Events:
  Type    Reason            Age   From                   Message
  ----    ------            ----  ----                   -------
  Normal  SuccessfulCreate  12s   replicaset-controller  Created pod: test-rs-z2qv7
  Normal  SuccessfulCreate  12s   replicaset-controller  Created pod: test-rs-654rx
```

Po dwugkrotnej próbie dodania poda z [pod-test-rs.yaml](pod-test-rs.yaml), kubernetes "ubijał" mojego poda:

```
$ k describe rs test-rs 
Name:         test-rs
...
Events:
  Type    Reason            Age                From                   Message
  ----    ------            ----               ----                   -------
  Normal  SuccessfulCreate  3m                 replicaset-controller  Created pod: test-rs-z2qv7
  Normal  SuccessfulCreate  3m                 replicaset-controller  Created pod: test-rs-654rx
  Normal  SuccessfulDelete  13s (x2 over 32s)  replicaset-controller  Deleted pod: new-rs
```

## Jak zadziała minReadySeconds bez readiness i liveliness probes?
Wykorzystujac [depoyment-without-probs.yaml](depoyment-without-probs.yaml), w którym parametr minReadSeconds został ustawiony na 30, otrzymałem poniższe efekty:

1. Pody wstaly po ok 7 sekundach
2. Po kolejnych 30, stan deploymentu wygladał nastepujaco
```
NAME           READY   UP-TO-DATE   AVAILABLE   AGE
helloapp-dep   1/2     2            1           40s
```
3. I dopiero po ok 80 wszyskto wygladało tak jak powinno:
```
NAME           READY   UP-TO-DATE   AVAILABLE   AGE
helloapp-dep   2/2     2            2           2m13s
```

Tak wiec kubernetes pomimo nie posiadania probes czeka zadany czas.

## Do czego może Ci się przydać matchExpressions?
Do definiowania bardziej skomplikowanych reguł, aby np pody które moga "chodzic" na devie nie "chodizły" na prodzie, ot taki przykład mi przyszedł na mysl.

## Jak najlepiej (według Ciebie) zarządzać historią zmian w deploymentach?
No na pewno należy podawać addnotacje i oczywiscie plik yaml powinien byc przetrzymywany w repo.

## Co się stanie jak usuniesz ReplicaSet stworzony przez Deployment?
Wówczas Kubernetes tworzy automatycznie pody, "nie doporowadzając" do usunięcia RS.

## Czy Pod może definiować więcej etykiet niż ReplicaSet ma zdefiniowane w selectorze?
Tak może, przykład: [replica-set-more-labels-pod.yaml](replica-set-more-labels-pod.yaml)

## Czy ReplicaSet może definiować więcej etykiet w selektorze niz Pod ma zdefiniowane?
Nie może, przykład: [replica-set-more-labels-rs.yaml](replica-set-more-labels-rs.yaml)
```
$ k apply -f replica-set-more-labels-rs.yaml 
The ReplicaSet "test-rs" is invalid: spec.template.metadata.labels: Invalid value: map[string]string{"tier":"test-rs"}: `selector` does not match template `labels`
```