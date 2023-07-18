# VimKube
A simple vim plugin to assist with "simple" Kubernetes tasks

## Requirements

- Vim 8.1+

- python 3.8+

- [kubernetes library](https://pypi.org/project/kubernetes)

Install with

```
pip install kubernetes
```

Be sure that the pip version you are using corresponds to vim's.

## Install 

Install using your favorite pluggin manager:

```
call vundle#begin()
...
Plugin 'codingismycraft/VimKube'
...
call vundle#end()            
```

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

## Object represenation

The plugin is aware of the following kubernetes concepts:

### Context (enclosed in "")

A context name is always enclosed in double quotes as can be 
see in this example:

```
"my-context-name"
```

### Service (enclosed in '')

A service name is always encloded in single quotes.

```
"my-application-name"
```

### Deployed tag (enclosed in <>)

A deployed tag is always enclosed in brakets. 

```
<my-tag>
```

# Interaction with the user

All the intraction with the user is done by a single keyboard combination (the
default is <leader>k).

When pressing the <leader>k combo the following different cases exist:

###  A window other than the one used by the pluggin is active

A new window with all the context names is opened.


### The cursor lies on the name of a context.

The pluggin window gets populated by all the services and their deployed tag 
on the context.


### The cursor lies on the name of a service.

The pluggin window gets populated with all the deployed tags for the service
(accross all the available contexts).

