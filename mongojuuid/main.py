from typing import List

import mongojuuid
import typer

app = typer.Typer()

@app.command(help=mongojuuid.to_bindata.__doc__)
def to_bindata(uuids: List[str]):
    for bindata in mongojuuid.to_bindata(*uuids):
        typer.echo(bindata)


@app.command(help=mongojuuid.to_uuid.__doc__)
def to_uuid(bindatas: List[str]):
    for uuid in mongojuuid.to_uuid(*bindatas):
        typer.echo(uuid)