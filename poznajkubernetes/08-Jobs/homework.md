# Wracając do Twojej aplikacji, albo twojej „wirtualnej” aplikacji, zastanów się:

## Do czego przydałby się CrobJob?
Sporo rzeczy w moim bieżącym projekcie musi być wykonywane cyklicznie:
- jakieś "sprawdzenia"
- robienie backupy
- migracje danych
- czyszczenie cacheow

## Czy widzisz bezpośrednie (bez CronJob) użycie Job?
Tak, przy zarządzaniu środowiskami testowymi, gdyż raz na jakiś czas muszę "odświeżyć środowisko" i zaakutalizować bazę danych.