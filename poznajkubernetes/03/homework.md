Skoro już wiesz jak działa przekazywanie konfiguracji do aplikacji w K8s, zastanów się i opisz (najlepiej na Slack), co w swojej aplikacji byś gdzie umieścił. Do dyspozycji masz:

# Zmienne środowiskowe
Zmienne środowiskowe użyłbym do przekazania np. typu środowiska DEV/TEST/PROD etc. oraz do definiowania jakiś stałych (ale takich naprawdę stałych) 
Niestety nie miałem okazji pracować w małych i krótkich projektach, ale znając swój projekt nie przesadzałbym z pewnoscią z liczbą zmiennych :)

# ConfigMap
Do konfig mapy z pewnością nadają się wszystkie pliki konfiguracyjne aplikacji.

# Secrets
W sumie to miałbym opory aby trzymać tam hasła i nazwy użytkownika, lecz wydaje mi się to dobre miejsce na jakieś connection stringi itp.

# Zewnętrzne narzędzia integrujące się z K8s
No własnie hasła i wszystkie dane wrażliwe, btw własnie mamy otwartą dyskusje na temat nowego systemu w którym przetrzymywać będziemy takie dane gdyż stary idzie na śmienitk i z mojej strony zaproponowałem własnie Vaulta :)

