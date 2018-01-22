# JFTT-Tester
Prosty tester dla kompilatorów na JFTT 2017

### Co to robi? ###
Tester składa się z dwóch części:
**Tester**

Przy pomocy podanego kompilatora (testowanego) kompiluje przykładowe pliki z katalogu **./in**, a następnie porównuje wyniki z interpretera dla tak otrzymanego pseudo-assemblera z z oczekiwanymi. Na razie testów nie ma zbyt wiele, ale łatwo dorabia się kolejne

W sytuacji gdy któryś test się wysypie, drukowane jest info o tym, który to test. Zwracana jest też ogólna informacja o powodzie niepowodzenia (błąd kompilacji, niewłaściwa zwracana wartość, rzucony wyjątek)


**Fuzzer (by Piotr Piotr)**

W skrócie - testuje tak długo aż coś się wywali - generuje losowe kody źródłowe, wrzuca w kompilator, porównuje z oczekiwanym wynikiem. Metoda sprawdzania identyczna jak w testerze, ale testy są prostsze. Pozwala wychwycić więcej corner-case'ów dla warunków logicznych i operacji arytmetycznych. Nie testuje pętli *while*.


### Czego to nie robi? (jeszcze) ###
* Nie mierzy czasu (choć może będzie dawać jakieś przydatne info o czasach w przyszłości)
* Nie obsługuje zamierzonych błędów kompilacji tzn. programów, które nie powinny dać się skompilować. To będzie niedługo zapewne
* Nie testuje jeszcze większości ficzerów, jakie ma mieć kompilator (głównie dlatego, że mój jest jeszcze w powijakach i nie mam jak testować)
* Nie informuje dobrze o rzuconych wyjątkach (info jest szczątkowe ale wiadomo, który plik powoduje problem, więc można potem testować ręcznie)

### Czego to nie będzie robić? ###
* Na pewno nie będzie żadnego sprawdzania kodu jakości/długości/wydajności pośredniego generowanego przez kompilator.


### Jak to uruchomić? ###
**Tester**
`python3 tester.py --compiler <ścieżka_do_kompilatora> --interpreter <ścieżka_do_interpretera>`
Program musi zostać uruchomiony dokładnie w tym katalogu, w którym jest plik **tester.py**, bo inaczej względne ścieżki wybuchną. Po wszelkie info odsyłam do **--help**

**Fuzzer**
`python3 fuzz/run.py <ścieżka_do_kompilatora> <ścieżka_do_interpretera>`
Fuzzer musi być uruchomiony z katalogu jak powyżej, bo inaczej wybuchnie.

Mogliśmy zrobić jednolity interfejs do obu programów, ale ~~nam się nie chciało~~ mieliśmy bardzo dużo pracy.

### Żaden test mi nie przechodzi, pomocy! ###
Obecnie wspierane są trzy tryby działania kompilatora, każdy z nich zakłada, że kod źródłowy jest podawany na stdin:
* kod pośredni może być zwracany na **stdout**, jest to tryb domyślny i nie trzeba podawać żadnej flagi aby to działało
* kod pośredni może być zwracany do pliku, którego nazwa jest podawana jako parametr przy wywołaniu kompilatora (ale nie jako nazwany parametr, to może później). Ten tryb wymaga podania flagi **--compiler_out_to_param_file**
* kod pośredni może być zwracany do pliku, którego nazwa jest stała i taka sama dla każdego pliku. Wówczas należy ustawić flagę **--compiler_out_to_const_file** i jako wartość podać ścieżkę do pliku wynikowego, do którego zwracać będzie kompilator. Należy się tutaj liczyć z faktem, że tester będzie na bieżąco ten plik usuwać po każdym teście.

**UWAGA** tryb 2. i 3. są jeszcze eksperymentalne - dodałem je, ale nie testowałem ich jeszcze na niczym, bo mój kompilator nie działa w ten sposób. Być może nie działają. Poczekam aż znajdzie się ktoś na tyle odważny, aby to sprawdzić albo sam to zrobię za jakiś czas.

Aby tester dobrze działał ważne jest też, aby kompilator zwracał **0**, jeżeli proces kompilacji się powiódł oraz dowolną niezerową wartość w przeciwnym wypadku (wartość zwracana w **main**)


Jeżeli kompilator działa w dokładnie ten sposób, to upewnij się, że podane ścieżki są poprawne. Jeżeli wciąż nie działa - skontaktuj się ze mną.


### Niektóre testy trwają tak długo, że blokują mi wywołanie pozostałych. Jak żyć? ###
Opcje są dwie:
* zoptymalizuj kod generowany przez kompilator. Żaden test nie został stworzony z intencją blokowania, więc coś działa Ci za wolno
* Jak Ci się nie chce w tym momencie, to możesz dodać nazwę pliku do słownika w pliku **ignored.py** (jest tam przykład), co sprawi, że test nie będzie uruchamiany.


### Jak dodać nowy test? ###
Trzeba zrobić **dwie** rzeczy:
* napisać kod źródłowy, który będzie inputem dla kompilatora
* dodać odpowiedni wpis w słowniku **main** w pliku **tests.py** analogicznie do innych wpisów, które tam są. Pole **input** to lista stringów, która zostanie wrzucona do uruchomionego programu (a więc będą łapane przez rozkaz **GET**). Pole **output** to lista linii, jakie powinien zwrócić program (ale mocno wygolony, najlepiej przyjrzeć się innym przykładom i zrobić analogicznie)
