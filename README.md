# BD - Builtins Defang

A quick and dirty POC for performing analysis on Python malware samples by intercepting `builtin.exec`. 

Typically, malware will be obfuscated in stack strings and encoding (like base64) before being decoded and called by `exec`. By executing everything up to `exec`, we can quickly and efficiently decode the intended payload.

I could not find any similar projects but perhaps I'm not searching well enough.

## Warning

I'm not convinced this method of overriding builtins is totally safe.

I have implemented a reasonable failsafe to prevent unwanted execution. Currently BD can only handle samples with one import (which is base64) and one call (which is exec). Poor little fella. This means you can't even BD `bd.py`.

## Usage

Requires Python. Tested with Python3.13.

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
kmsec@penguin:~/analysis/bd$ python bd.py test.sample 
🤖 Processing test.sample
🤖 This sample imports base64 as base64
🤖 ❗ Permitted call to `exec` in the context of base64
🤖 Intercepted call to `exec` with the following payload:

``` ``` ```
b'print("I\'m a haxxor")'
``` ``` ```

🤖 Done with test.sample
```