1. Co się stanie gdy nadamy taki sam klucz? Czego Ty byś się spodziewał?
Nie mozemy stworzyć CM z takim samym kluczem, tak było to spodziewane.

2. Czy można nadać dowolną nazwę klucza w ConfigMap?
Nie, tak jak niżej:
$ k create cm cm-04  --from-literal=hehe.][hehe=value1
error: "hehe.][hehe" is not a valid key name for a ConfigMap: a valid config key must consist of alphanumeric characters, '-', '_' or '.' (e.g. 'key.name',  or 'KEY_NAME',  or 'key-name', regex used for validation is '[-._a-zA-Z0-9]+')

