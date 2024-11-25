# Witam witam i o zdrowie pytam
Obecna wersja `README.md` jest skierowana do użytku wewnętrznego. W niej niesamowite jakościowe rzeczy:
## Zarządzamy pakietami
### yapping
Od dzisiaj wspólnie zarządzamy pakietami. Może późno, ale musimy to robić 
- żeby móc integrować razem i mieć pewność, że operujemy na tych samych falach
- żeby przygotować aplikację do wydania (odpalenia w środowisku zewnętrznym, przez kogoś z zewnątrz)

Do tego będziemy używać takiego narzędzia jak `pyproject.toml`, jako iż jest to oficjalny format PyPI i Pythona. Plik ma łatwą strukturę, polecam się zapoznać. Interesjące są sekcje `dependencies` oraz `[project.optional-dependencies]`. Idea jest taka, że w dependencies będą pakiety wspólne, a w _optional_ takie konkretnie do odpalenia notebooków np, albo aplikacji z UI. 
Po co podział? Do integracji naszych pakietów na tym etapie oraz potem do skreślenia tych, które były potrzebne tylko na etapie developmentu. Odchudzi to listę wymaganych pakietów. Nadmienię jeszcze, że obecnie pakiety nie są do końca posegregowane, listę da się podzielić dokładniej. Zachęcam do dodawania waszych pakietów i integrowania powoli wszystkiego. Przypominam, że zainstalowane pakiety i wersje można podejrzeć np. poleceniem `pip freeze`. Zachęcam do dodawania wersji, bo może być niemiła niespodzianka z brakiem wstecznej kompatybilności nowszych wersji. Koniec gadania.
### aktywacja środowiska
1. (_opcjonalnie_) Zachęcam do korzystania z managera pakietów np. condy i uprzedniego stworzenia `conda create --name  >to_środowisko< python=3.10` i aktywowania środowiska docelowego `conda activate >to_środowisko<`.
2. Jak już mamy to środowisko docelowe (`(>to_środowisko<)` wyświetlane w linii w terminalu w przypadku condy o tym świadczy), to lecimy z pythonkiem:
`python -m pip install --upgrade pip`
najnowsza dostępna wersja pipa (tylko raz trzeba w sumie)
3. I tak instalujemy pakiety:
- `python -m pip install .` instaluje podstawowe zależności 
- `python -m pip install -e .[gui]` instaluje podstawower + opcjonalne zależności z danej grupy 

To propozycja, zachęcam do sugestii i zmian :).

## Dokumentacja
Zachęcam do używania VSC i instalacji wszystkiego tak jak w [tym poradniku](https://www.youtube.com/watch?v=4lyHIQl4VM8&t=320s). Potem nie ręczę za nieprzyjmności (may God have mercy on you). Pliki są w folderze `doc`, przykładowy pdf na discordzie. Nie przejmujcie się błędami, jak .pdf śmiga to wszystko śmiga. Występujące rozdziały, ich podział i kolejność to kolejna propozycja, która wymaga Waszego rozważenia i sugestii :)) 