"""
Rekx is a command line interface to Kerchunk
"""
from rich.panel import Panel
import typer
from .typer_parameters import OrderCommands
from .diagnose import get_netcdf_metadata
from .diagnose import collect_netcdf_metadata
from .diagnose import diagnose_chunking_shapes
from .diagnose import determine_common_chunking_layout
from .consistency import check_chunk_consistency
from .consistency import check_chunk_consistency_json
from .suggest import suggest_chunking_shape
from .suggest import suggest_chunking_shape_alternative
from .suggest import suggest_chunking_shape_alternative_symmetrical
from .rechunk import modify_chunk_size
from .rechunk import rechunk
from .rechunk import generate_rechunk_commands
from .rechunk import generate_rechunk_commands_for_multiple_netcdf
from .reference import create_kerchunk_reference
from .parquet import parquet_reference
from .parquet import parquet_multi_reference
from .combine import combine_kerchunk_references
from .combine import combine_kerchunk_references_to_parquet
from .parquet import combine_parquet_stores_to_parquet
from .select import read
from .select import select_fast
from .select import select_time_series
from .select import select_time_series_from_json
from .select import select_time_series_from_json_in_memory
from .parquet import select_from_parquet
from .parquet import read_from_parquet
from .rich_help_panel_names import rich_help_panel_diagnose
from .rich_help_panel_names import rich_help_panel_suggest
from .rich_help_panel_names import rich_help_panel_rechunking
from .rich_help_panel_names import rich_help_panel_reference
from .rich_help_panel_names import rich_help_panel_combine
from .rich_help_panel_names import rich_help_panel_select
from .rich_help_panel_names import rich_help_panel_select_references
from rekx.messages import NOT_IMPLEMENTED_CLI


def version_callback(value: bool):
    if value:
        typer.echo("Rekx CLI Version: 1.0.0")  # Replace with your actual version
        raise typer.Exit()


typer.rich_utils.Panel = Panel.fit
app = typer.Typer(
    cls=OrderCommands,
    add_completion=True,
    add_help_option=True,
    no_args_is_help=True,
    rich_markup_mode="rich",
    help=f"🙾  🦖 Rekx command line interface [bold][magenta]prototype[/magenta][/bold]",

)


# callback

@app.callback()
def callback_app(
    version: bool = typer.Option(
        None, "--version", callback=version_callback,
        is_eager=True, help="Show the version and exit."
    )
):
    pass


# diagnose

app.command(
    name='inspect',
    help='Inspect an Xarray-supported dataset',
    no_args_is_help=True,
    rich_help_panel=rich_help_panel_diagnose,
)(get_netcdf_metadata)
app.command(
    name='inspect-multiple',
    help='Inspect multiple Xarray-supported data',
    no_args_is_help=True,
    rich_help_panel=rich_help_panel_diagnose,
)(collect_netcdf_metadata)
app.command(
    name='shapes',
    help='Diagnose chunking shapes in multiple Xarray-supported data',
    no_args_is_help=True,
    rich_help_panel=rich_help_panel_diagnose,
)(diagnose_chunking_shapes)
app.command(
    name='common-shape',
    help='Determine common chunking shape in multiple Xarray-supported data',
    no_args_is_help=True,
    rich_help_panel=rich_help_panel_diagnose,
)(determine_common_chunking_layout)

# validate chunking in series of data

app.command(
    name="validate",
    help='Validate chunk size consistency along multiple Xarray-supported data',
    no_args_is_help=True,
    rich_help_panel=rich_help_panel_diagnose,
)(check_chunk_consistency)
app.command(
    name='validate-json',
    help='Validate chunk size consistency along multiple Kerchunk reference files [reverse]How to get available variables?[/reverse]',
    no_args_is_help=True,
    rich_help_panel=rich_help_panel_diagnose,
)(check_chunk_consistency_json)

# suggest

app.command(
    name='suggest',
    no_args_is_help=True,
    help=f"Suggest a good chunking shape, [yellow]ex.[/yellow] [code]'8784,2600,2600'[/code] [reverse]Needs a review![/reverse]",
    rich_help_panel=rich_help_panel_suggest,
)(suggest_chunking_shape)
app.command(
    name="suggest-alternative",
    no_args_is_help=True,
    help='Suggest a good chunking shape [red]Merge to [code]suggest[/code][/red]',
    rich_help_panel=rich_help_panel_suggest,
)(suggest_chunking_shape_alternative)
app.command(
    name="suggest-symmetrical",
    no_args_is_help=True,
    help='Suggest a good chunking shape [red]Merge to [code]suggest[/code][/red]',
    rich_help_panel=rich_help_panel_suggest,
)(suggest_chunking_shape_alternative_symmetrical)

# rechunk 

app.command(
    name="modify-chunks",
    help=f'Modify in-place the chunk size metadata in NetCDF files {NOT_IMPLEMENTED_CLI}',
    no_args_is_help=True,
    rich_help_panel=rich_help_panel_rechunking,
)(modify_chunk_size)
app.command(
    name="rechunk",
    help=f'Rechunk data',
    no_args_is_help=True,
    rich_help_panel=rich_help_panel_rechunking,
)(rechunk)
# app.command(
#     name="rechunk-generator",
#     help=f'Generate variations of rechunking commands [green bold]Work-In-Progress[/green bold]',
#     no_args_is_help=True,
#     rich_help_panel=rich_help_panel_rechunking,
# )(generate_rechunk_commands)
app.command(
    name="rechunk-generator",
    help=f'Generate variations of rechunking commands for multiple files',
    no_args_is_help=True,
    rich_help_panel=rich_help_panel_rechunking,
)(generate_rechunk_commands_for_multiple_netcdf)

# create reference sets

app.command(
    name="reference",
    help='Create Kerchunk JSON reference files',
    no_args_is_help=True,
    rich_help_panel=rich_help_panel_reference,
)(create_kerchunk_reference)
app.command(
    "reference-parquet",
    no_args_is_help=True,
    help=f"Create Parquet references to an HDF5/NetCDF file [red]Merge to [code]reference[/code][/red]",
    rich_help_panel=rich_help_panel_reference,
)(parquet_reference)
app.command(
    "reference-multi-parquet",
    help=f"Create Parquet references to multiple HDF5/NetCDF files [red]Merge to [code]reference-parquet[/code][/red]",
    no_args_is_help=True,
    rich_help_panel=rich_help_panel_reference,
)(parquet_multi_reference)

# combine reference sets

app.command(
    name="combine",
    help='Combine Kerchunk reference sets (JSONs to JSON)',
    no_args_is_help=True,
    rich_help_panel=rich_help_panel_combine,
)(combine_kerchunk_references)
app.command(
    name="combine-to-parquet",
    help="Combine Kerchunk reference sets into a single Parquet store (JSONs to Parquet)",
    no_args_is_help=True,
    rich_help_panel=rich_help_panel_combine,
)(combine_kerchunk_references_to_parquet)
app.command(
    'combine-parquet-stores',
    help=f"Combine multiple Parquet stores (Parquets to Parquet)",
    no_args_is_help=True,
    rich_help_panel=rich_help_panel_combine,
)(combine_parquet_stores_to_parquet)

# select / read

app.command(
    name="select",
    help='  Select time series over a location',
    no_args_is_help=True,
    rich_help_panel=rich_help_panel_select,
)(select_time_series)
app.command(
    name="select-fast",
    help='  Bare read time series from Xarray-supported data and optionally write to CSV [bold magenta reverse] :timer_clock: Performance Test [/bold magenta reverse]',
    no_args_is_help=True,
    rich_help_panel=rich_help_panel_select,
)(select_fast)
app.command(
    name="read",
    help='  Bare read time series from Xarray-supported data [bold magenta reverse] :timer_clock: Performance Test [/bold magenta reverse]',
    no_args_is_help=True,
    rich_help_panel=rich_help_panel_select,
)(read)
app.command(
    name="select-json",
    help='  Select time series over a location from a JSON Kerchunk reference set',
    no_args_is_help=True,
    rich_help_panel=rich_help_panel_select_references,
)(select_time_series_from_json)
app.command(
    name="select-json-from-memory",
    help='  Select time series over a location from a JSON Kerchunk reference set in memory',
    no_args_is_help=True,
    rich_help_panel=rich_help_panel_select_references,
)(select_time_series_from_json_in_memory)
app.command(
    name='select-parquet',
    help=f" Select data from a Parquet references store",
    no_args_is_help=True,
    rich_help_panel=rich_help_panel_select_references,
)(select_from_parquet)
app.command(
    name='read-parquet',
    help=f" Read data from a Parquet references store [bold magenta reverse] :timer_clock: Performance Test [/bold magenta reverse]",
    no_args_is_help=True,
    rich_help_panel=rich_help_panel_select_references,
)(read_from_parquet)


if __name__ == "__main__":
    app()
