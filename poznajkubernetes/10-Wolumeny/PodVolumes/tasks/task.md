# Przypomnij sobie jak działa emptyDir i hostPath. Powtórz ćwiczenia z lekcji Kontenery typu Init – ćwiczenia dla utrwalenia informacji. Możesz zmodyfikować zadanie by pobierać i cachować repozytorium git z wykorzystaniem hostPath.

To w ramach przypomnienia napisałem konficurację zawartą w pliku: [clone-git-repo.yaml](clone-git-repo.yaml)

# Wykonaj dwa zadania z subPath (dla ułatwienia skorzystaj z ConfigMap):

## Spróbój nadpisać plik /etc/udhcpd.conf i zweryfikuj czy jego zawartosć jest poprawna i czy zawartość innych plików w katalogu jest poprawna.
Do tego przykładu został wykorzystany plik konfiguracyjny [subpath-udhcpd.yaml](subpath-udhcpd.yaml)

Zazwyczaj ten plim wygląda mniej wiecej tak:
```
$ k exec -it sub-path /bin/sh
~ $ cd /etc/^C
~ $ cat etc/udhcpd.conf
# Sample udhcpd configuration file (/etc/udhcpd.conf)
# Values shown are defaults

# The start and end of the IP lease block
start		192.168.0.20
end		192.168.0.254

# The interface that udhcpd will use
interface	eth0

# The maximum number of leases (includes addresses reserved
# by OFFER's, DECLINE's, and ARP conflicts). Will be corrected
# if it's bigger than IP lease block, but it ok to make it
# smaller than lease block.
#max_leases	254

# The amount of time that an IP will be reserved (leased to nobody)
# if a DHCP decline message is received (seconds)
#decline_time	3600
```

Po skonfigurowaniu CM, możemy zauważyć ze plik został nadpisany:
```
$ k exec -it sub-path /bin/sh
~ $ cat /etc/udhcpd.conf 
jakas dziwna wartosc
```

## Zrób to samo dla pliku /usr/bin/wget
Do tego przykładu została uzyta konfiguracja: [subpath-wget.yaml](subpath-wget.yaml)

Po nadpisaniu pliku /usr/bin/wget nie mogę się dostać do kontenera:
```
$ k exec -it sub-path-wget /bin/sh
OCI runtime exec failed: exec failed: container_linux.go:345: starting container process caused "exec: \"/bin/sh\": permission denied": unknown
command terminated with exit code 126
```
