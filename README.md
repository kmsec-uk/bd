# BD - Builtins Defang

A quick and dirty POC for performing analysis on Python malware samples.

I could not find any similar projects but perhaps I'm not searching well enough.

## Warning

I'm not convinced this is totally safe.

## Usage

```
python bd.py [-h] <file>
```

## Example

Example `test_sample` contents:

```
import base64
example = 'cHJpbnQoIkknbSBhIGhheHhvciIp'
d = base64.b64decode(example)
exec(d)
```

`bd.py` output:

```bash
kmsec@penguin:~/analysis/bd$ python bd.py test_sample 
🤖 Processing test_sample
🤖 This sample imports base64 as base64
🤖 ❗ Executing in the context of base64
🤖 Intercepted exec:

```` ``` ````
b'print("I\'m a haxxor")'
```` ``` ````
🤖 Done with test_sample
```