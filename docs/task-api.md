## Task API
Task is stored as JSON and has the following structure:

```json5
{
  // could be an empty array
  "articles": ['doi_1', 'doi2'],
  // Other content fields depend on type
  "content": {
    "type": 'OpenEnded'
  },
  "scoring": {
    "model": 'Exact'
  },
  "cognitiveType": ''
}
```

Scoring models:
- Exact - checks if the answer is exactly the same as the reference
- AI - involves AI model to check if the answer is correct according to the instructions

```json5
{
  "model": 'Exact'
}
```
```json5
{
  "model": 'AI'
}
```

For OpenEnded type:

```json5
{
  "type": 'OpenEnded',
  "text": 'Task text',
  "referenceSolution": 'Solution text'
}
```