# Tools

## quicktest_client.py

HTTP client with hardcoded stuff to quickly test the workloads.
Assumes MinIO is already deployed (as usual).
```console
$ tools/quicktest_client.py --help
```
Example:
```console
$ HOSTPORT='147.102.4.12:31493' tools/quicktest_client.py json_serdes
```
