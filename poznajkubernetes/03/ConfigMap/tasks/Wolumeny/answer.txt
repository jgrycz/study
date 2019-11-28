Pod został utworzony zgodnie z poleceniem
$ k exec pkad -- ls /config/cm-02/
config1.cfg
key1
konfig_2

$ k exec pkad -- ls  /config/cm-03/
30KB.cfg
40KB.cfg
50KB.cfg
    
1. Co się stanie jak z mountPath ustawisz na katalog Twojej aplikacji?
W podzie z pliku pod-etc.yaml, mountPath ustawiłem na /etc/network i wszystkie pliki z tej lokacji zostały nadpisane

2. Co się stanie jak plik stworzony przez ConfigMap zostanie usunięty? Czy taki plik zostanie usunięty? co spowoduje aktualizacja ConfigMapy?

a)
Nie możemy usunąc takiego pliku:
$ k exec pkad -- rm /etc/network/key1
rm: can't remove '/etc/network/key1': Read-only file system
command terminated with exit code 1

b) wartosc zostanie zaaktualizowana:
$ k exec pkad -- cat /etc/network/key1
val1

$ k edit cm cm-02 
configmap/cm-02 edited

$ k exec pkad -- cat /etc/network/key1
nowa_wartosc
