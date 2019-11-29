# Praca z ConfigMap
1. Stwórz ConfigMap wykorzystując kubectl
 - Załącz do niej przynajmniej dwie proste wartości (literal)
 - Załącz do niej klucz: 123_TESTING z dowolną wartością
 - Załącz do niej klucz: TESTING-123 z dowolną wartością
 - Załącz do niej klucz: TESTINGz dowolną wartością

```
$ k create cm cm-01 --from-literal=key1=val1 --from-literal=key2=val2 --from-literal=123_TESTING=1000 --from-literal=TESTING-123=milion --from-literal=TESTING=1000
configmap/cm-01 created
```

Output- [cm-01.yaml](cm-01.yaml)

2. Stwórz drugą ConfigMap wykorzystując kubectl
 - Załącz do niej dwie takie same klucze i ale różne wartości
 - Jeden plik normalnie
 - Oraz jeden plik z inną nazwą klucza niż nazwa pliku

```
$ k create cm cm-02 --from-literal=key1=val1 --from-literal=key1=val2 --from-file=config1.cfg --from-file=konfig_2=config2.cfg
error: cannot add key "key1", another key by that name already exists in Data for ConfigMap "cm-02"
$ k create cm cm-02 --from-literal=key1=val1 --from-file=config1.cfg --from-file=konfig_2=config2.cfg
configmap/cm-02 created
```

Output- [cm-02.yaml](cm-02.yaml)

3. Stwórz trzecią ostatnią ConfigMapę wykorzystując kubectl
 - zrób tak by załączyć pliki o rozmiarach ~20KB, ~30KB, ~40KB i ~50KB

Output- [cm-03.yaml](cm-03.yaml)

```
$ k create cm cm-03 --from-file=config3-20KB.cfg --from-file=config3-30KB.cfg --from-file=config3-40KB.cfg --from-file=config3-50KB.cfg
$
```

Duze configi:
[20KB](config3-20KB.cfg) [30KB](config3-30KB.cfg) [40KB](config3-40KB.cfg) [50KB](config3-50KB.cfg)


Wyeksportuj wszystkie stworzone ConfigMapy do yamli.

# Co się stanie gdy nadamy taki sam klucz? Czego Ty byś się spodziewał?
Nie mozemy stworzyć CM z takim samym kluczem, tak było to spodziewane.

# Czy można nadać dowolną nazwę klucza w ConfigMap?

Nie, tak jak niżej:

```
$ k create cm cm-04  --from-literal=hehe.][hehe=value1
error: "hehe.][hehe" is not a valid key name for a ConfigMap: a valid config key must consist of alphanumeric characters, '-', '_' or '.' (e.g. 'key.name',  or 'KEY_NAME',  or 'key-name', regex used for validation is '[-._a-zA-Z0-9]+')
```