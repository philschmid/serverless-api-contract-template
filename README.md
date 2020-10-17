# Template for a new Knative Python Serivce

## Getting Started

**git clone**

```bash
git clone https://github.com/coc-buml/buml-knative-python-template.git <new-service-name>
```

**init project**

```bash
poetry init
```

**init virtual env**

```bash
poetry shell
```

**install after clone**

```bash
poetry install
```

**scripts**

**Aliasing** `alias poe='poetry run poe'`

```bash
poetry run poe start
```

**install packages**

```bash
poetry add <package>
```

**install dev packages**

```bash
poetry add --dev <package>
```

**deactivate virtual env**

```bash
deactivate
```

**format**

```bash
black .
```

**lint**

```bash
pylama
```

**type check**

```bash
mypy .
```

**pydoc string**

```bash
pydocstyle src
```

**test**

```bash
pytest
```

**build**

```bash
docker build . -t <image-name>
```

**run**

```bash
docker run -d  -p internal:external <image-name>
```

## Async await in python

https://fastapi.tiangolo.com/async/

## References

https://github.com/nsidnev/fastapi-realworld-example-app/blob/master/app/main.py
https://mypy.readthedocs.io/en/stable/getting_started.html#installing-and-running-mypy
