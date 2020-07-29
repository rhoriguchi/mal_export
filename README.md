# mal_export

This project runs with python3.

It logs in to [MyAnimeList](https://myanimelist.net/) with the specified user and extracts the watched status of all tv shows and saves them as json.

## Install

python setup.py install

## Run

If no `configPath` is given, it searches in current directory for `config.yaml`.

```bash
mal_export [configPath]
```

## config.yaml

If no `sava_path` is given, it exports to current dir.

```yaml
username: ****
password: ****
sava_path: /tmp/exports
```
