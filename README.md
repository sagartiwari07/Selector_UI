# Data-Downloader Server

```http
GET /login
```

| Parameter  | Type     | Description                     |
|:-----------|:---------|:--------------------------------|
| `email`    | `string` | **Required**. Client's email    |
| `password` | `string` | **Required**. Client's password |

## Responses

```javascript
{
  "message": string,
}
```

The `message` attribute contains a string commonly used to indicate status of the request.

## Status Codes

Server returns the following status codes in its response:

| Status Code | Description             |
|:------------|:------------------------|
| 200         | `OK`                    |
| 400         | `BAD REQUEST`           |
| 401         | `UNAUTHORIZED`          |
| 500         | `INTERNAL SERVER ERROR` |

#

```http
GET /device_details
```

## Responses

```javascript
{
  "message": string,
  "data": list
}
```

The `message` attribute contains a message commonly used to indicate status of the request.

The `data` attribute contains a list of json objects in the following format

```javascript
{
  "device_name": string,
  "col_name": string,
  "doc_count": int,
  "data_size": string
}
```

## Status Codes

Server returns the following status codes in its response:

| Status Code | Description             |
|:------------|:------------------------|
| 200         | `OK`                    |
| 403         | `ACCESS RESTRICTED`     |
| 500         | `INTERNAL SERVER ERROR` |

#

```http
POST /data
```

| Parameter     | Type   | Description                                                                          |
|:--------------|:-------|:-------------------------------------------------------------------------------------|
| `devices`     | `list` | **Required**. List containing the collection name of the devices                     |
| `query`       | `list` | **Required**. List containing queries                                                |
| `save_as_one` | `bool` | **Required**. Whether to save each device's data as an individual file or as a whole |

## Responses

```javascript
{
  "message": string,
  "data": json
}
```

The `message` attribute contains a string commonly used to indicate status of the request.

The `data` attribute contains a json object in the following format

```javascript
{
  "path": string,
  "row": int,
  "column": int,
  "preview": json
}
```
The `path` attribute should be used in the `/download/<path>` to download the file. The file will only be available for 5 minutes.

The `preview` attribute is the `head` of the resulted data file which then converted into a dictionary.

## Status Codes

Server returns the following status codes in its response:

| Status Code | Description             |
|:------------|:------------------------|
| 200         | `OK`                    |
| 400         | `BAD REQUEST`           |
| 403         | `ACCESS RESTRICTED`     |
| 500         | `INTERNAL SERVER ERROR` |

#

```http
GET /download/<path>
```

## Responses

Downloads the requested file under the name `data.zip` . In case of any error, the following response will be sent

```javascript
{
  "message": string,
}
```

The `message` attribute contains a string commonly used to indicate status of the request.

## Status Codes

Server returns the following status codes in its response:

| Status Code | Description             |
|:------------|:------------------------|
| 404         | `NOT FOUND`             |
| 403         | `ACCESS RESTRICTED`     |
| 500         | `INTERNAL SERVER ERROR` |

#

```http
GET /logout
```

## Responses

```javascript
{
  "message": string,
}
```

The `message` attribute contains a string commonly used to indicate status of the request.

## Status Codes

Server returns the following status codes in its response:

| Status Code | Description             |
|:------------|:------------------------|
| 200         | `OK`                    |
| 403         | `ACCESS RESTRICTED`     |
| 500         | `INTERNAL SERVER ERROR` |

#
