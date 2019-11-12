# Praca domowa - moduł 1

# Krótki wstep na temat projektu w którym pracuje

Aplikacja bankowa rozwijana od ~20 lat w cpp, wykonująca pewien rodzaj kalkulacji, na prodzie ok 80 VMek, komunikacja między procesami jest obsługiwana przez ACE TAO (jest to implementacja standardu CORBA, 20 lat temu było to modne ponoć) oraz gRPC. Wybiegając troche do przodu, na prodowych maszynach nie mamy możliwości mieć jeszcze kubernetesa oraz dockera... (wiec też ten kurs nie jest po to aby uprościć moją prace w tej firmię, ale żeby móc zmienić pracę :) ) wykorzystujemy baze Oracla która posiada >30TB danych

## Jakie praktyki z 12Factor mój projekt aktualnie spełnia?
## Jakich praktyk z 12Factor nie spełnia?

Przepraszam ale wszystko omówiłem w jednym ciągu. :)

1. Codebase:
    Tak, jeszcze svn.
2. Dependencies:
    Zależności są spakowane w 2 dużych paczkach ~2GB, dystrubucja tych paczek jest wymagana na każdej maszynie, wiec uznałbym ten punkt za spełniony lecz nie podoba mi się sposób.
3. Konfiguracja:
    Raczej tak, configi ze wzglądu na na swoją objętość są przetrzymywane w repo (oddzielnym od kodu). Mamy wyspecyfikowanych kilka typów testowych oraz PRODa, jak i klona PRODa który jest identycznie skonfigurowany jak prod, gdzie używamy tylko innych bazdanych itp. Co do danych wrażliwych, to mamy zewnętrzny tool który hasła. Tak więc wydaje mi się, że ten wymóg jest spełniony.
4. Backing services:
    Tutaj ciężko mi to określić, owszem mamy dużą baze, wymiana instancji jest bardzo prosta, a ze względu na specyfikę pracy banku wszystko jest wewnętrznie zarządzane to nawet nie potrafię sobie wyobrazć, że uzywamy S3 od Amazona, czy czegoś innego.
5. Build, release, run:
    Tylko build, budujemy po każdym commicie, automatyczne i czeste dostarczenia mam zamiar wdrożyć w niedługim czasie. Deployment jest robiony przez wewnętrzny skrypt, który ma opcje szybkiego przywórcenia poprzedniej wersji, w sumie nic też nie stoi na przeszkodzie posiadania kilku wersji appki, lecz w danym środowisku tylko jedna może być używana w jednocześnie.
6. Processes:
    Tak/nie, Mamy kilka komponentów które muszą działać jako singleton, lecz reszta komponentów jest bezstanowa i mamy możliwość uruchomić dany komponent w wielu instancjach.
7. Port binding:
    Cięzko mi powiedzieć gdyż aplikacja którą wspieram nie jest aplikacją internetową. Komunikacja obsługiwana przez ACE TAO jest dla nas niewidoczna dlatego też porty po których porozumiewają się procesy nie są wybierane "przezemnie", co do komponętów które komunikują się po gRPC to w configu mamy zapisany port po którym mogą gadać. Wyjście na świat (a raczej bank) odbywa się przez load balanecera, który forwarduje requesty do kolejki. Tak więc LB/uzytkownik nie wie jaki worker, gdzie będzie wykonywał zadanie wszytko też się dzieje asynchronicznie, dlatego też nie musimy utrzymywać półączenia przez cały czas przetwarzania requestu.
8. Concurrency:
    Tak, komponenty typu singleton są skalowalne w ten sposób, wystarczy przestawić odpowiedni parametr w configu.
9. Disposability:
    Tak, Procesy startują bardzo szybko, wszystkie też mają zaprogramowaną obłsuge sigterm'a, po to aby np zrzucic zkeszowane dane do bazy.
10. Dev/Prod parity:
    hmm, ze względu na wielkość Proda nie jest mozliwe utrzymywanie podobnych środowisk (aczkolwiek mamy jednego pełnego klona), lecz śrowodiwska testerskie posiadają mininalny set procesów/komponentów które są wymagane do wykonania pewnych kalkulacji. Na srodowiskach testowych uzywamy takich samych baz danych z mniejsza liczbą danych, a także bazy nie maja takiego samego performancu. Wdrażanie na proda to porażka, sam release trwa nawet kilka godzin, ale to też ze wzgledu na to, że zewnętrzne projekty musza sie z nami zsynchronizować, jest jeszcze sporo do poprawy, przynajmniej z mojej strony, ale sporo bankowych restrykcji robi swoje.
11. Logs:
    Tak, procesy z defaulta piszą na stdout, lecz podczas uruchamiania ich przekierowujemy output do <nazwa_komponętu>.<PID>.<data>.<hash>, lecz nie mamy żadnego ELK czy SPLUNka
12. Admin process:
    Nie, m.in. migracje są wykonywane przez zewnętrzny zespół z Indi

## Czy mogę tak zmodyfikować projekt, by spełniał wszystkie praktyki 12Factor?

Jest sporo do poprawy, nad cześcią już pracuje, migracja do git'a, automatyczne deploymenty (ale nie na proda), lecz wydjae mi się, że specyfika banku niepozowla na to aby wszystkie punkty były spełnione.

## Dlaczego nie mogę, co stoi na przeszkodzie?

Procesy wew.

## Czy jest sens spełniać wszystkie praktyki 12Factor w aktualnym projekcie?

W sumie to nie wiem :)

## Czy architektura rozwiązania umożliwi konteneryzację?

Kontenerów uzywam np, do budowania apki i w paru innych miejscach. Lecz w tym momencie nie wiem czy juz wymienione wczesniej TAO ma możliwośc pracy w kontenerze, bo jak wtedy zapewnić "sharowanie" portów, a pozatym i tak na prodzie nie możemy mieć dockera... 

## Dlaczego nie? Co mogę zrobić, by jednak dało się zrobić konteneryzację? Albo jakie kroki mogę podjąć już teraz by w kolejnych projektach takich problemów nie mieć?

Jakby TAO, wspierało kontneryzacje (czego nie wiem, ale obawiam się, że nie wspiera)to nic nie stałoby na przeszkodzie aby wpakowac poszczególne komponęty w konetenery, a samo użycie k8s na pewno usprawniłoby procesy zwiazane z DR które teraz są manualnie przetwarzane.