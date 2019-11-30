# Wykonaj podstawowe operacje na etykietach imperatywnie. Takie operacje będą przydatne w późniejszych częściach szkolenia jak na przykład trzeba będzie przeanalizować niedziałający Pod albo przekierować ruch na inne Pody.

- Dodaj etykietę
```
$ k label pod pkad env=prod
pod/pkad labeled

$ k get pods --show-labels 
NAME   READY   STATUS      RESTARTS   AGE   LABELS
bb     0/1     Completed   0          24m   name=bb
pkad   1/1     Running     0          23m   env=prod,name=pkad
```

- Dodaj etykietę do wszystkich zasobów na raz
```

$ k label pod --all version=1.2.3
pod/bb labeled
pod/pkad labeled

$ k get pods -L version
NAME   READY   STATUS      RESTARTS   AGE   VERSION
bb     0/1     Completed   0          25m   1.2.3
pkad   1/1     Running     0          25m   1.2.3
```

- Zaktualizuj etykietę
```
$ k label pod pkad --overwrite env=test
pod/pkad labeled

$ k get pods -L env
NAME   READY   STATUS      RESTARTS   AGE   ENV
bb     0/1     Completed   0          26m   
pkad   1/1     Running     0          26m   test
```

- Usuń etykietę
```
$ k label pod pkad env-
pod/pkad labeled

$ k get pods -L env
NAME   READY   STATUS      RESTARTS   AGE   ENV
bb     0/1     Completed   0          28m   
pkad   1/1     Running     0          27m 
```

# Stwórz trzy Pody z czego dwa posiadające po dwie etykiety: app=ui i env=test oraz app=ui i env=stg, trzeci bez etykiet

PODy:
 - [pod1](pod1.yaml)
 - [pod2](pod2.yaml)
 - [pod3](pod3.yaml)

- Wybierz wszystkie Pody które mają etykietę env zdefiniowaną
```
$ k  get pods -l env --show-labels 
NAME    READY   STATUS    RESTARTS   AGE   LABELS
pkad1   1/1     Running   0          46s   app=ui,env=test
pkad2   1/1     Running   0          43s   app=ui,env=stg
```

- Wybierz wszystkie Pody które nie mają etykiety env zdefiniowanej
```
$ k get pod --selector '!env' --show-labels 
NAME    READY   STATUS    RESTARTS   AGE     LABELS
pkad3   1/1     Running   0          2m57s   <none>
```

- Wybierz Pody które mają app=ui ale nie znajdują się w env=stg
```
$ k get pod -l app=ui,env!=stg --show-labels 
NAME    READY   STATUS    RESTARTS   AGE     LABELS
pkad1   1/1     Running   0          4m15s   app=ui,env=test
```

- Wybierz Pody których env znajduje się w przedziale stg i demo
```
$ k get pod --selector 'env in (stg, demo)' --show-labels 
NAME    READY   STATUS    RESTARTS   AGE     LABELS
pkad2   1/1     Running   0          5m30s   app=ui,env=stg

```

# Z wcześniej stworzonych Podów:
- Wybierz i wyświetl tylko nazwy Poda
```
$ k get pod -o jsonpath='{.items[*].metadata.name}'
pkad1 pkad2 pkad3
```

- Posortuj widok po dacie ostatniej aktualizacji Poda
```
$ k get pod --sort-by=.metadata.creationTimestamp
NAME    READY   STATUS    RESTARTS   AGE
pkad1   1/1     Running   0          12m
pkad2   1/1     Running   0          12m
pkad3   1/1     Running   0          12m
```

- Wybierz tylko i wyłączenie te Pody które nie są w fazie Running
```
$ k get pods
NAME    READY   STATUS      RESTARTS   AGE
bb      0/1     Completed   0          3m31s
pkad1   1/1     Running     0          17m
pkad2   1/1     Running     0          17m
pkad3   1/1     Running     0          17m

$ k get pods --field-selector status.phase!=Running
NAME   READY   STATUS      RESTARTS   AGE
bb     0/1     Completed   0          3m48s

```
