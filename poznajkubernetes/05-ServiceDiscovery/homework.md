# Praca domowa

Bazując na wiedzy z poprzednich modułów możesz teraz przeanalizować w jaki sposób udostępniać aplikacje sieciowo w klastrze i po za klastrem. Jeżeli nie masz swojego systemu, to wykonaj mentalne ćwiczenie „jakie wartości fajnie by było mieć”.

 - Czy będzie korzystać z Service Discovery? Jeśli tak to jakiego? Dlaczego?
    Service Discovery to jest coś co chciałbym u siebie w aplikacji wdrożyć, po to aby uniknąć, "statycznej" konfiguracji.
 - Jakie typy serwisu wykorzysta do Services wykorzystasz? Dlaczego?
    Zakładając, że uzywałbym K8S to w bieżacej aplikacji widze możliwość użycia każdego z typów servisów, oczywiscie w zależności od wymagań, m.in do tasków które komunikują się wewnątrz klastra wystarczy ClusterIP
 - Do publikacji aplikacji użyjesz NodePort czy LoadBalancer? Dlaczego?
    W sumie to nie wiem czego bym uzył wszystko zależy od sytuacji, LB wydaje mi się lepszym rozwiązaniem do bardziej skomplikowanych architektur 
