regulator = 3;

plikAB = fopen('AB.txt','r');           % wiersze pliku "AB.txt" to 6-elementowe wektory cech
wektorAB = fscanf(plikAB, '%f', 6);     
wektorAB = transpose(wektorAB);
daneAB = wektorAB;
status = feof(plikAB);
while ~status
    wektorAB = fscanf(plikAB, '%f', 6);
    wektorAB = transpose(wektorAB);
	daneAB = vertcat(daneAB, wektorAB);
    status = feof(plikAB);
end
status = fclose(plikAB);                % od teraz zmienna "daneAB" to macierz odpowiadaj¹ca zawartoœci pliku "AB.txt"
ileAB = size(daneAB);                   % wiersze macierzy "daneAB" to kolejne wektory cech, kolumny macierzy "daneAB" to kolejne cechy tych wektorów - kolumn jest 6
ileAB = ileAB(1);                       % zmienna "ileAB" zawiera liczbê wierszy macierzy "daneAB" - czyli liczba wektorów cech
wzorzecAB = mean(daneAB,1);             % "wzorzecAB" to wektor 6 cech œrednich

plikNO = fopen('NO.txt','r');
wektorNO = fscanf(plikNO, '%f', 6);
wektorNO = transpose(wektorNO);
daneNO = wektorNO;
status = feof(plikNO);
while ~status
    wektorNO = fscanf(plikNO, '%f', 6);
    wektorNO = transpose(wektorNO);
    daneNO = vertcat(daneNO, wektorNO);
    status = feof(plikNO);
end
status = fclose(plikNO);
ileNO = size(daneNO);
ileNO = ileNO(1);
wzorzecNO = mean(daneNO,1);

plikDH = fopen('DH.txt','r');
wektorDH = fscanf(plikDH, '%f', 6);
wektorDH = transpose(wektorDH);
daneDH = wektorDH;
status = feof(plikDH);
while ~status
    wektorDH = fscanf(plikDH, '%f', 6);
    wektorDH = transpose(wektorDH);
	daneDH = vertcat(daneDH, wektorDH);
    status = feof(plikDH);
end
status = fclose(plikDH);
ileDH = size(daneDH);
ileDH = ileDH(1);
wzorzecDH = mean(daneDH,1);

plikSL = fopen('SL.txt','r');
wektorSL = fscanf(plikSL, '%f', 6);
wektorSL = transpose(wektorSL);
daneSL = wektorSL;
status = feof(plikSL);
while ~status
    wektorSL = fscanf(plikSL, '%f', 6);
    wektorSL = transpose(wektorSL);
	daneSL = vertcat(daneSL, wektorSL);
    status = feof(plikSL);
end
status = fclose(plikSL);
ileSL = size(daneSL);
ileSL = ileSL(1);
wzorzecSL = mean(daneSL,1);


for i = 1:1:ileAB                                   % pêtla po ka¿dym wierszu macierzy "daneAB"
    dane2AB = daneAB;                               % macierz "dane2AB" to kopia macierzy "daneAB"
    wektor = dane2AB(i,:);                          % pobieram z macierzy "dane2AB" i-ty wiersz do zmiennej "wektor"
    dane2AB(i,:) = [];                              % usuwam z macierzy "dane2AB" i-ty wiersz
    wzorzec2AB = mean(dane2AB,1);                   % dla macierzy "dane2AB" tworze nowy wzorzec, jego elementy jako wartoœci œrednie nie uzglêdniaj¹ elementów wiersza usuniêtego
    
    % w poni¿szej pêtli sprawdzê, czy wektor usuniêty z macierzy "dane2AB"
    % ponownie bêdzie do niej pasowa³, gdy porównam go z jej nowym wzorcem
    % "wzorzec2AB".
    odlABwart = 0;
    for j = 1:1:6
        odlAB(j) = abs(wektor(j) - wzorzec2AB(j));
        odlABwart = odlABwart + odlAB(j)*odlAB(j);
    end
    odlABwart = sqrt(odlABwart);
    
    odlNOwart = 0;
    for j = 1:1:6
        odlNO(j) = abs(wektor(j) - wzorzecNO(j));
        odlNOwart = odlNOwart + odlNO(j)*odlNO(j);
    end
    odlNOwart = sqrt(odlNOwart);
    
    odlDHwart = 0;
    for j = 1:1:6
        odlDH(j) = abs(wektor(j) - wzorzecDH(j));
        odlDHwart = odlDHwart + odlDH(j)*odlDH(j);
    end
    odlDHwart = sqrt(odlDHwart);
    
    odlSLwart = 0;
    for j = 1:1:6
        odlSL(j) = abs(wektor(j) - wzorzecSL(j));
        odlSLwart = odlSLwart + odlSL(j)*odlSL(j);
    end
    odlSLwart = sqrt(odlSLwart);
    
    min = odlABwart;
    if min > odlNOwart
        %min = odlNOwart;
        k = 0;
        for j = 1:1:6
            if odlAB(j) < odlSL(j)
                k = k + 1;
            end
        end
        if k < regulator
            min = odlNOwart;
        end
    end
    if min > odlDHwart
        %min = odlDHwart;
        k = 0;
        for j = 1:1:6
            if odlAB(j) < odlDH(j)
                k = k + 1;
            end
        end
        if k < regulator
            min = odlDHwart;
        end
    end
    if min > odlSLwart
        %min = odlSLwart;
        k = 0;
        for j = 1:1:6
            if odlAB(j) < odlSL(j)
                k = k + 1;
            end
        end
        if k < regulator
            min = odlSLwart;
        end
    end
    
    if min == odlABwart
        sprawdzAB(i) = 1;
    else
        sprawdzAB(i) = 0;
    end
end


for i = 1:1:ileNO
    dane2NO = daneNO;
    wektor = dane2NO(i,:);
    dane2NO(i,:) = [];
    wzorzec2NO = mean(dane2NO,1);
    
    odlABwart = 0;
    for j = 1:1:6
        odlAB(j) = abs(wektor(j) - wzorzecAB(j));
        odlABwart = odlABwart + odlAB(j)*odlAB(j);
    end
    odlABwart = sqrt(odlABwart);
    
    odlNOwart = 0;
    for j = 1:1:6
        odlNO(j) = abs(wektor(j) - wzorzec2NO(j));
        odlNOwart = odlNOwart + odlNO(j)*odlNO(j);
    end
    odlNOwart = sqrt(odlNOwart);
    
    odlDHwart = 0;
    for j = 1:1:6
        odlDH(j) = abs(wektor(j) - wzorzecDH(j));
        odlDHwart = odlDHwart + odlDH(j)*odlDH(j);
    end
    odlDHwart = sqrt(odlDHwart);
    
    odlSLwart = 0;
    for j = 1:1:6
        odlSL(j) = abs(wektor(j) - wzorzecSL(j));
        odlSLwart = odlSLwart + odlSL(j)*odlSL(j);
    end
    odlSLwart = sqrt(odlSLwart);
    
    min = odlNOwart;
    if min > odlABwart
        %min = odlABwart;
        k = 0;
        for j = 1:1:6
            if odlNO(j) < odlAB(j)
                k = k + 1;
            end
        end
        if k < regulator
            min = odlABwart;
        end
    end
    if min > odlDHwart
        %min = odlDHwart;
        k = 0;
        for j = 1:1:6
            if odlNO(j) < odlDH(j)
                k = k + 1;
            end
        end
        if k < regulator
            min = odlDHwart;
        end
    end
    if min > odlSLwart
        %min = odlSLwart;
        k = 0;
        for j = 1:1:6
            if odlNO(j) < odlSL(j)
                k = k + 1;
            end
        end
        if k < regulator
            min = odlSLwart;
        end
    end
    
    if min == odlNOwart
        sprawdzNO(i) = 1;
    else
        sprawdzNO(i) = 0;
    end
end


for i = 1:1:ileDH
    dane2DH = daneDH;
    wektor = dane2DH(i,:);
    dane2DH(i,:) = [];
    wzorzec2DH = mean(dane2DH,1);
    
    odlABwart = 0;
    for j = 1:1:6
        odlAB(j) = abs(wektor(j) - wzorzecAB(j));
        odlABwart = odlABwart + odlAB(j)*odlAB(j);
    end
    odlABwart = sqrt(odlABwart);
    
    odlNOwart = 0;
    for j = 1:1:6
        odlNO(j) = abs(wektor(j) - wzorzecNO(j));
        odlNOwart = odlNOwart + odlNO(j)*odlNO(j);
    end
    odlNOwart = sqrt(odlNOwart);
    
    odlDHwart = 0;
    for j = 1:1:6
        odlDH(j) = abs(wektor(j) - wzorzec2DH(j));
        odlDHwart = odlDHwart + odlDH(j)*odlDH(j);
    end
    odlDHwart = sqrt(odlDHwart);
    
    odlSLwart = 0;
    for j = 1:1:6
        odlSL(j) = abs(wektor(j) - wzorzecSL(j));
        odlSLwart = odlSLwart + odlSL(j)*odlSL(j);
    end
    odlSLwart = sqrt(odlSLwart);
    
    min = odlDHwart;
    if min > odlNOwart
        %min = odlNOwart;
        k = 0;
        for j = 1:1:6
            if odlDH(j) < odlNO(j)
                k = k + 1;
            end
        end
        if k < regulator
            min = odlNOwart;
        end
    end
    if min > odlABwart
        %min = odlABwart;
        k = 0;
        for j = 1:1:6
            if odlDH(j) < odlAB(j)
                k = k + 1;
            end
        end
        if k < regulator
            min = odlABwart;
        end
    end
    if min > odlSLwart
        %min = odlSLwart;
        k = 0;
        for j = 1:1:6
            if odlDH(j) < odlSL(j)
                k = k + 1;
            end
        end
        if k < regulator
            min = odlSLwart;
        end
    end
    
    if min == odlDHwart
        sprawdzDH(i) = 1;
    else
        sprawdzDH(i) = 0;
    end
end


for i = 1:1:ileSL
    dane2SL = daneSL;
    wektor = dane2SL(i,:);
    dane2SL(i,:) = [];
    wzorzec2SL = mean(dane2SL,1);
    
    odlABwart = 0;
    for j = 1:1:6
        odlAB(j) = abs(wektor(j) - wzorzecAB(j));
        odlABwart = odlABwart + odlAB(j)*odlAB(j);
    end
    odlABwart = sqrt(odlABwart);
    
    odlNOwart = 0;
    for j = 1:1:6
        odlNO(j) = abs(wektor(j) - wzorzecNO(j));
        odlNOwart = odlNOwart + odlNO(j)*odlNO(j);
    end
    odlNOwart = sqrt(odlNOwart);
    
    odlDHwart = 0;
    for j = 1:1:6
        odlDH(j) = abs(wektor(j) - wzorzecDH(j));
        odlDHwart = odlDHwart + odlDH(j)*odlDH(j);
    end
    odlDHwart = sqrt(odlDHwart);
    
    odlSLwart = 0;
    for j = 1:1:6
        odlSL(j) = abs(wektor(j) - wzorzec2SL(j));
        odlSLwart = odlSLwart + odlSL(j)*odlSL(j);
    end
    odlSLwart = sqrt(odlSLwart);
    
    min = odlSLwart;
    if min > odlNOwart
        %min = odlNOwart;
        k = 0;
        for j = 1:1:6
            if odlSL(j) < odlNO(j)
                k = k + 1;
            end
        end
        if k < regulator
            min = odlNOwart;
        end
    end
    if min > odlDHwart
        %min = odlDHwart;
        k = 0;
        for j = 1:1:6
            if odlSL(j) < odlDH(j)
                k = k + 1;
            end
        end
        if k < regulator
            min = odlDHwart;
        end
    end
    if min > odlABwart
        %min = odlABwart;
        k = 0;
        for j = 1:1:6
            if odlSL(j) < odlAB(j)
                k = k + 1;
            end
        end
        if k < regulator
            min = odlABwart;
        end
    end
    
    if min == odlSLwart
        sprawdzSL(i) = 1;
    else
        sprawdzSL(i) = 0;
    end
end


jedenAB = 0;
zeroAB = 0;
for i = 1:1:ileAB
    if sprawdzAB(i) == 1
        jedenAB = jedenAB + 1;
    else
        zeroAB = zeroAB + 1;
    end
end


jedenNO = 0;
zeroNO = 0;
for i = 1:1:ileNO
    if sprawdzNO(i) == 1
        jedenNO = jedenNO + 1;
    else
        zeroNO = zeroNO + 1;
    end
end


jedenDH = 0;
zeroDH = 0;
for i = 1:1:ileDH
    if sprawdzDH(i) == 1
        jedenDH = jedenDH + 1;
    else
        zeroDH = zeroDH + 1;
    end
end


jedenSL = 0;
zeroSL = 0;
for i = 1:1:ileSL
    if sprawdzSL(i) == 1
        jedenSL = jedenSL + 1;
    else
        zeroSL = zeroSL + 1;
    end
end