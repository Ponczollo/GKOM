# GKOM Zima 2026
Tutaj powinny znaleźć się informacje odnośnie organizacji kodu oraz sposobie uruchamiania/instalacji projektu.

## Setup
Wersja Python - do ustalenia

#### Linux
```bash
python -m venv .venv
source ./.venv/bin/activate
```
#### Windows
```PowerShell
python -m venv .venv
./.venv/Scripts/Activate.ps1
```

## Git
Proponuję strukturę branchy typu {typ}/{opis}
Opis to wiadomo, typy to powiedzmy:
- feat
- fix
- refactor
- docs

Branch per task na pewno nie wyjdzie thou fajnie gdyby chodź było to ustrukturyzowane. Typu żeby na jednym branchu nie było jednocześnie nowej mechaniki gry, update'u tekstur i fixów do wcześniejszego kodu