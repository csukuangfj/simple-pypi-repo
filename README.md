## Usage

```
git clone https://github.com/csukuangfj/simple-pypi-repo
./simple-pypi-repo/update-page.py --dst nightly
```

Wheels are uploaded to `./nightly/whl`, where `nightly` is a symlink 
to `/var/www/k2-fsa/nightly`.

Whenever a file is uploaded to `./nightly/whl`, `./nightly/index.html`
is updated.

See <https://k2-fsa.org/> and <https://k2-fsa.org/nightly/index.html>
