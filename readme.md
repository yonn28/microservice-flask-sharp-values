##### setting a debugger create folder .venv

1.
`````
python3 -m venv .venv
`````
2
activate enviroment

`````
. .venv/bin/activate 

```

4. configure launcer with the name of the index.py  of entry, and the python path

`````
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Attach using Process Id",
            "type": "python",
            "request": "attach",
            "processId": "${command:pickProcess}"
        },
        {
            "name": "Python: Flask",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "index.py",
                "FLASK_ENV": "development"
            },
            "args": [
                "run",
                "--no-debugger"
            ],
            "jinja": true,
            "python.pythonPath": ".venv/bin/python3"
        }
    ]
}

````

5. configure settings.json with the python path

``````
{
    "python.testing.unittestArgs": [
        "-v",
        "-s",
        ".",
        "-p",
        "test_*.py"
    ],
    "python.testing.pytestEnabled": false,
    "python.testing.nosetestsEnabled": false,
    "python.testing.unittestEnabled": true,
    "python.pythonPath": ".venv/bin/python3"
}

````
6. change the python interpreter for take into de account the virtual enviroment in vscode is with ctl + shift + python
set this to the folder .env/bin/python3

with all this you can make your debug