# lambda-client

## Requirements

To install, you need Python 3 and PIP. Then:

```
pip3 install -r requirements.txt
```

## Configuration

Edit `lambda.conf` and fill in your private and public IDs:

```
[SECRET]
PrivateKey = <your private id>  
PublicKey = <your public id>                  
```

## Usage

First, run the daemon:

```
./lambdad.py
```

Then, in a separate terminal, you can execute `lambda-cli` commands. For
example:

NB: paths passed to `./lambda-cli.py submit` are interpreted relative to the
daemon process, not to the CLI process.