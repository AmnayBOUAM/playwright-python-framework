# playwright-python-framework

Projet perso pour monter en compétence sur **Playwright** en Python, sur le site de démo
[saucedemo.com](https://www.saucedemo.com).

En cours de construction.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install
cp .env.example .env
```

## Lancer les tests

```bash
pytest
pytest -m smoke
pytest --headed --slowmo 500
```

Rapport HTML : `reports/report.html`
