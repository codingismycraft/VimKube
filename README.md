# VimKube
A simple vim plugin to assist with "simple" Kubernetes tasks

## Skipping a context

If you need to skip some contexts from processing you can do so by adding its
name to .kubelens.json configuration file under the home directory.

The contents of this file can look as follows:

```json
{
    "contexts-to-skip": [
        "content-name..",
        ....
    ]
}
```

