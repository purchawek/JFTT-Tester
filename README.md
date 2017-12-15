# JFTT-Tester
Prosty tester dla kompilatorów na JFTT 2017

### Co to robi? ###
Przy pomocy podanego kompilatora (testowanego) kompiluje przykładowe pliki z katalogu **./in**, a następnie porównuje wyniki z interpretera dla tak otrzymanego pseudo-assemblera z z oczekiwanymi. Na razie testów nie ma zbyt wiele, ale łatwo dorabia się kolejne

W sytuacji gdy któryś test się wysypie, drukowane jest info o tym, który to test. Zwracana jest też ogólna informacja o powodzie niepowodzenia (błąd kompilacji, niewłaściwa zwracana wartość, rzucony wyjątek)


### Czego to nie robi? (jeszcze) ###
* Nie mierzy czasu (choć może będzie dawać jakieś przydatne info o czasach w przyszłości)
* Nie obsługuje zamierzonych błędów kompilacji tzn. programów, które nie powinny dać się skompilować. To będzie niedługo zapewne
* Nie testuje jeszcze większości ficzerów, jakie ma mieć kompilator (głównie dlatego, że mój jest jeszcze w powijakach i nie mam jak testować)
* Nie informuje dobrze o rzuconych wyjątkach (info jest szczątkowe ale wiadomo, który plik powoduje problem, więc można potem testować ręcznie)

### Czego to nie będzie robić? ###
* Na pewno nie będzie żadnego sprawdzania kodu jakości/długości/wydajności pośredniego generowanego przez kompilator.


### Jak to uruchomić? ###
**python3 tester.py**
Program musi zostać uruchomiony dokładnie w tym katalogu, w którym jest plik **tester.py**, bo inaczej względne ścieżki wybuchną. Po wszelkie info odsyłam do **--help**


### Jak dodać nowy test? ###
Trzeba zrobić **dwie** rzeczy:
* napisać kod źródłowy, który będzie inputem dla kompilatora
* dodać odpowiedni wpis w słowniku **main** w pliku **tests.py** analogicznie do innych wpisów, które tam są. Pole **input** to lista stringów, która zostanie wrzucona do uruchomionego programu (a więc będą łapane przez rozkaz **GET**). Pole **output** to lista linii, jakie powinien zwrócić program (ale mocno wygolony, najlepiej przyjrzeć się innym przykładom i zrobić analogicznie)
