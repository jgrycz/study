#1. Co ma pierwszeństwo: zmienna środowiskowa zdefiniowana w ConfiMap czy w Pod?

Bazujac na Podzie z pliku [pod.yaml](pod.yaml), wyglada na to, że pierwszeństwo mają zmienne z ConfigMapy

```
$ k exec pkad -- printenv
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOSTNAME=pkad
CM2_CFG1=jakis
  taki
    dziwny
  ten
config

CM2_CFG2=ten
tez
jakis
dziwny

TESTING=1000
TESTING-123=milion
key1=val1
key2=val2
TEST=TEST_HEHE
KUBERNETES_PORT_443_TCP_ADDR=10.96.0.1
KUBERNETES_SERVICE_HOST=10.96.0.1
KUBERNETES_SERVICE_PORT=443
KUBERNETES_SERVICE_PORT_HTTPS=443
KUBERNETES_PORT=tcp://10.96.0.1:443
KUBERNETES_PORT_443_TCP=tcp://10.96.0.1:443
KUBERNETES_PORT_443_TCP_PROTO=tcp
KUBERNETES_PORT_443_TCP_PORT=443
HOME=/
```
#2. Czy kolejność definiowania ma znaczenie (np.: env przed envFrom)?
                                      
Tak ma, potwierdzają to pody [pod.yaml](pod.yaml) i [pod-changed-order.yaml](pod-changed-order.yaml)
```
$ k exec pkad -- printenv
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOSTNAME=pkad
CM2_CFG1=jakis
  taki
    dziwny
  ten
config

CM2_CFG2=ten
tez
jakis
dziwny

TESTING=1000
TESTING-123=milion
key1=val1
key2=val2
TEST=TEST_HEHE
KUBERNETES_PORT_443_TCP_ADDR=10.96.0.1
KUBERNETES_SERVICE_HOST=10.96.0.1
KUBERNETES_SERVICE_PORT=443
KUBERNETES_SERVICE_PORT_HTTPS=443
KUBERNETES_PORT=tcp://10.96.0.1:443
KUBERNETES_PORT_443_TCP=tcp://10.96.0.1:443
KUBERNETES_PORT_443_TCP_PROTO=tcp
KUBERNETES_PORT_443_TCP_PORT=443
HOME=/
```

#3. Jak się ma kolejność do dwóch różnych ConfigMap?

Podczas zdefiniowania zmiennych "naprzemiennie" patrz [pod-cm-order.yaml](pod-cm-order.yaml), zmienne zostały wczytane zgodnie z taką samą kolejnością:

```
$ k exec pkad -- printenv
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOSTNAME=pkad
CM1_ENV1=1000
CM2_ENV1=jakis
  taki
    dziwny
  ten
config

CM1_ENV2=1000
CM2_ENV2=ten
tez
jakis
dziwny

CM1_ENV3=milion
KUBERNETES_SERVICE_PORT_HTTPS=443
KUBERNETES_PORT=tcp://10.96.0.1:443
KUBERNETES_PORT_443_TCP=tcp://10.96.0.1:443
KUBERNETES_PORT_443_TCP_PROTO=tcp
KUBERNETES_PORT_443_TCP_PORT=443
KUBERNETES_PORT_443_TCP_ADDR=10.96.0.1
KUBERNETES_SERVICE_HOST=10.96.0.1
KUBERNETES_SERVICE_PORT=443
HOME=/
```

