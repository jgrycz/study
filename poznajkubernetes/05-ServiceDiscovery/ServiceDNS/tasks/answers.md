# Service Discovery – Ćwiczenia

Przetestuj działanie Service Discovery korzystając ze swojej aplikacji albo helloapp.

Definicja podów i serwisów znajduje się w pliku: [myapp.yaml](myapp.yaml)

 - Utwórz dwa namespaces
```
$ k create ns ns1
namespace/ns1 created

$ k create ns ns2
namespace/ns2 created
```

 - W każdym namespaces umieć pod i serwis

```
$ k apply -f myapp.yaml -n ns1
pod/myapp created
pod/tools created
service/myoapp created

$ k apply -f myapp.yaml -n ns2
pod/myapp created
pod/tools created
service/myapp created

$ k get pods --all-namespaces 
...
ns1           myapp                                 1/1     Running   0          2m20s
ns1           tools                                 1/1     Running   0          2m20s
ns2           myapp                                 1/1     Running   0          2m16s
ns2           tools                                 1/1     Running   0          2m16s

$ k get svc --all-namespaces 
NAMESPACE     NAME         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                  AGE
default       kubernetes   ClusterIP   10.96.0.1        <none>        443/TCP                  24m
kube-system   kube-dns     ClusterIP   10.96.0.10       <none>        53/UDP,53/TCP,9153/TCP   26d
ns1           myapp        ClusterIP   10.102.186.121   <none>        80/TCP                   2m44s
ns2           myapp        ClusterIP   10.106.57.100    <none>        80/TCP                   2m40s
```

 - Przetestuj działanie Service Discovery z wykorzystaniem curl i nslookup. Jeśli używasz swojej aplikacji wywołaj endpointy pomiędzy aplikacjami.

```
$ k exec -it tools -n ns1 -- sh
/ # nslookup myapp
Server:		10.96.0.10
Address:	10.96.0.10#53

Name:	myapp.ns1.svc.cluster.local
Address: 10.102.186.121

/ # nslookup myapp.ns1
Server:		10.96.0.10
Address:	10.96.0.10#53

Name:	myapp.ns1.svc.cluster.local
Address: 10.102.186.121

/ # nslookup myapp.ns2
Server:		10.96.0.10
Address:	10.96.0.10#53

Name:	myapp.ns2.svc.cluster.local
Address: 10.106.57.100

$ k exec -it tools -n ns2 -- sh
/ # nslookup myapp
Server:		10.96.0.10
Address:	10.96.0.10#53

Name:	myapp.ns2.svc.cluster.local
Address: 10.106.57.100

/ # nslookup myapp.ns2
Server:		10.96.0.10
Address:	10.96.0.10#53

Name:	myapp.ns2.svc.cluster.local
Address: 10.106.57.100

/ # nslookup myapp.ns1
Server:		10.96.0.10
Address:	10.96.0.10#53

Name:	myapp.ns1.svc.cluster.local
Address: 10.102.186.121
```

Curlem też możemy się odpytac appki z innego namespace:
```
$ k exec -it tools -n ns1 -- sh
/ # curl myapp
<h1>Czołem!</h1>
/ # curl myapp.ns1
<h1>Czołem!</h1>
/ # curl myapp.ns2
<h1>Czołem!</h1>

$ k exec -it tools -n ns2 -- sh
/ # curl myapp
<h1>Czołem!</h1>
/ # curl myapp.ns1
<h1>Czołem!</h1>
/ # curl myapp.ns2
<h1>Czołem!</h1>
```