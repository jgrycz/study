# Obiekt serwisu – Ćwiczenia
## Ćwiczenie 1

Korzystając z wiedzy z lekcji przetestuj następujące scenariusze komunikacji:

 - container-to-container w Pod. Wykorzystaj do tego nginx.
    Korzystając z konfiguracji [container-to-container.yaml](container-to-container.yaml), byłem w stanie połączyć sie do kontenera myapp

```
   $ k exec -it myapp -c tools sh
/ # wget -q localhost
/ # cat index.html 
<h1>Czołem!</h1>

/ # 
```

 - Komunikacja pomiędzy Podami – Pod-to-Pod. Wykorzystaj do tego nginx.
    Wykorzystujac konfigurację z [pod-to-pod.yaml](pod-to-pod.yaml), mamy zaprezentowane poniżej połączenie typu pod-to-pod
   
```
$ k apply -f pod-to-pod.yaml 
pod/myapp created
pod/tools created

$ k get pods -o wide
NAME    READY   STATUS    RESTARTS   AGE   IP             NODE          NOMINATED NODE   READINESS GATES
myapp   1/1     Running   0          23s   10.244.0.157   master-node   <none>           <none>
tools   1/1     Running   0          23s   10.244.0.158   master-node   <none>           <none>

$ k exec -it tools sh

/ # wget -q 10.244.0.157
/ # cat index.html 
<h1>Czołem!</h1>
```

 - Wykorzystaj nginx i wystaw go za pomocą serwisu ClusterIP w środku klastra.
    Wykorzystano konfiguracje poda z [pod-to-pod.yaml](pod-to-pod.yaml) oraz service z [svc-clusterip.yaml](svc-clusterip.yaml)

```
$ k get svc
NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP    2d
myapp-svc    ClusterIP   10.108.18.165   <none>        7777/TCP   105s

$ k exec -it tools sh
/ # wget -q 10.108.18.165:7777
/ # cat index.html 
<h1>Czołem!</h1>
```

 - Wykorzystaj nginx i wystaw go na świat za pomocą serwisu NodePort w dwóch opcjach: bez wskazywania portu dla NodePort i ze wskazaniem.

   Bez wskazywania portu dla NodePort:

    Wykorzystano konfiguracje poda z [pod-to-pod.yaml](pod-to-pod.yaml) oraz service z [svc-nodeport.yaml](svc-nodeport.yaml)

```
$ k apply -f svc-nodeport.yaml 
service/myapp-http created

$ k get svc myapp-http 
NAME         TYPE       CLUSTER-IP    EXTERNAL-IP   PORT(S)        AGE
myapp-http   NodePort   10.104.81.1   <none>        80:32611/TCP   16s

$ curl localhost:32611
<h1>Czołem!</h1>

```

   Ze wskazaniem:

    Wykorzystano konfiguracje poda z [pod-to-pod.yaml](pod-to-pod.yaml) oraz service z [svc-nodeport-port.yaml](svc-nodeport-port.yaml)

```
$ k apply -f svc-nodeport-port.yaml 
service/myapp-http created

$ k get svc 
NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP        2d
myapp-http   NodePort    10.98.140.170   <none>        80:31111/TCP   3s

$ curl localhost:31111
<h1>Czołem!</h1>
```

 - Wykorzystaj nginx i wystaw go na świat za pomocą serwisu typu LoadBalancer

    Wykorzystano konfiguracje poda z [pod-to-pod.yaml](pod-to-pod.yaml) oraz service z [svc-loadbalancer.yaml](svc-loadbalancer.yaml)

```
$ k apply -f svc-loadbalancer.yaml 
service/myapp-http created

$ k get svc
NAME         TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
kubernetes   ClusterIP      10.96.0.1      <none>        443/TCP        2d
myapp-http   LoadBalancer   10.101.56.13   <localhost>     80:30326/TCP   5s

$ curl localhost
<h1>Czołem!</h1>
```


# Ćwiczenie 2

Utwórz dwa Pody z aplikacją helloapp, które mają po jednym wspólnym Label, oraz posiadają oprócz tego inne Label (poniżej przykład).
 
Przy konfiguracji takiej jak [double-pod.yaml](double-pod.yaml) oraz [svc-doublepod.yaml](svc-doublepod.yaml), odpowiadają obie instancje.

```
$ k apply -f double-pod.yaml 
pod/myapp-instance-1 created
pod/myapp-instance-2 created

$ k apply -f svc-doublepod.yaml 
service/double-pod-svc created

$ k describe svc 
double-pod-svc  kubernetes      

$ k get svc 
NAME             TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
double-pod-svc   NodePort    10.101.232.99   <none>        80:32746/TCP   29s
kubernetes       ClusterIP   10.96.0.1       <none>        443/TCP        2d1h

$ curl localhost:32746
<h1>Czołem z instancji 2!</h1>

$ curl localhost:32746
<h1>Czołem z instancji 2!</h1>

$ curl localhost:32746
<h1>Czołem z instancji 1!</h1>

$ curl localhost:32746
<h1>Czołem z instancji 1!</h1>
```

Przy konfiguracji takiej jak [double-pod.yaml](double-pod.yaml) oraz [svc-doublepod-v2-only.yaml](svc-doublepod-v2-only.yaml), odpowiada tylko druga instancja.

```
$ k apply -f svc-doublepod-v2-only.yaml 
service/double-pod-svc-v2 created

$ k get svc 
NAME                TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
double-pod-svc-v2   NodePort    10.110.189.181   <none>        80:30837/TCP   4s
kubernetes          ClusterIP   10.96.0.1        <none>        443/TCP        2d1h

$ curl localhost:30837
<h1>Czołem z instancji 2!</h1>

$ curl localhost:30837
<h1>Czołem z instancji 2!</h1>

$ curl localhost:30837
<h1>Czołem z instancji 2!</h1>

$ curl localhost:30837
<h1>Czołem z instancji 2!</h1>

$ curl localhost:30837
<h1>Czołem z instancji 2!</h1>

$ curl localhost:30837
<h1>Czołem z instancji 2!</h1>
```