[![Author][contributors-shield]][contributors-url]
[![BSD-3 Clause License][license-shield]][license-url]
![example workflow](https://github.com/RaphSku/metaqueue/actions/workflows/ci.yml/badge.svg)
[![Metaqueue CD](https://github.com/RaphSku/metaqueue/actions/workflows/cd.yml/badge.svg)](https://github.com/RaphSku/metaqueue/actions/workflows/cd.yml)

# metaqueue


### Goal
Efficiently run tasks concurrently and write metadata to a repository and write metainformation in a PostgresSQL database.

### How to install it
1. `pip install metaqueue`

### How to use it
1. Create tasks with any signature you like but this function has to fulfill two requirements, one is that you have to pass a `metadataengine` into the task and the other is that you have to declare it as async.
2. In order to push metadata to the metadataengine, you can use the following:
```python
metadataengine.publish_to_topic(Metadata(data, name, location, context))
```
The metadata is associated to a topic which defines what kind of metadata is collected by the metadataengine. Metadata consists of 4 attributes, the data itself, the name, the location and a context. 
Note that a metadataengine is defined as
```python
MetadataEngine(topic, queue)
```
where topic is an enum element and queue is a metaqueue. A metaqueue is like a queue but with extra functionality. You don't have to worry about it but it is useful to know how a metaqueue is defined.
```python
MetaQueue(buffer_size = 3, dtype = int)
```
You can provide a `buffer_size` which is the maximum capacity of the queue and `dtype` specifies which kind of data can be stored in it.
3. Now, you are ready to kickstart the `TaskRunner` which is running the defined tasks concurrently. You can use it in the following way
```python
await TaskRunner.run(async_funcs = [task1, task2], args = [task1_args, task2_args])
```
where the arguments are given as tuples into the list `args`. In this step, the tasks are not only run concurrently but also the metadata are collected via the metadataengine.
4. Afterwards, we can define a Metabroker which will then push the metadata to a repository and push the information associated to the metadata into the PostgreSQL database.
```python
connector  = StoreToLocalhost(path = "./log.txt")
metastore  = MetaStore(**db_info)
metabroker = MetaBroker(metadataengines = [engines[0], engines[1]], metastore = metastore, connector = connector)
metabroker.run(timeout = 10)
```
Up until now, only one connector is supported and that is a local file where the metadata gets written to. Since the MetaStore is using PostgreSQL as a database, you have to provide a running instance of that database. The easiest way is to spin up a docker container and pass the connection information to the MetaStore as `db_info`. `db_info` is a dict which contains the following keys: host, database, user, password, port. On the run method of the metabroker you can define a `timeout`. This should prevent running the metabroker for too long.
5. View the result, inside of your PostgreSQL database you should find your database with a table `metadata` in which you can find all the information associated to your metadata. Also, the log file should be created and contain all the metadata in a format which resembles the OpenMetrics format.
  
[contributors-url]: https://github.com/RaphSku
[license-url]: https://github.com/RaphSku/Metaqueue/blob/main/LICENSE

[contributors-shield]: https://img.shields.io/badge/Author-RaphSku-red
[license-shield]: https://img.shields.io/badge/License-BSD--3%20Clause-green
