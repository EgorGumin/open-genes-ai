## Task API
Task is stored as JSON and has the following structure:

```json5
{
  "id": 'uuid_v7 id',
  // could be an empty array
  "articles": ['doi_1', 'doi2'],
  // Other content fields depend on type
  "content": {
    "type": 'OpenEnded'
  }
}
```

For OpenEnded type:

```json5
{
  "type": 'OpenEnded',
  "text": 'String'
}
```