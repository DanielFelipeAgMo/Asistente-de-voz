from spoty.commands.first_list_commands import \
    count_command, \
    delete_command, \
    copy_command, \
    move_command, \
    export_command, \
    import_deezer_command, \
    import_spotify_command, \
    sync_spotify_command, \
    print_command, \
    create_m3u8_command
from spoty.utils import SpotyContext
import click


@click.group("get-unique")
@click.pass_obj
def get_unique(context: SpotyContext,               ):
    """
Get unique tracks (not duplicated) for further actions (see next commands).
    """

    context.summary.append("Collecting unique tracks:")

    context.tags_lists.clear()
    context.tags_lists.append([])

    context.tags_lists[0].extend(context.unique_first_tracks)
    context.summary.append(f'  {len(context.unique_first_tracks)} unique tracks collected.')

    if len(context.tags_lists[0]) == 0:
        context.summary.append(f'  0 unique tracks collected.')

    context.duplicates_groups = []
    context.unique_first_tracks = []
    context.unique_second_tracks = []

get_unique.add_command(count_command.count_tracks)
get_unique.add_command(print_command.print_tracks)
get_unique.add_command(export_command.export_tracks)
get_unique.add_command(create_m3u8_command.export_tracks)
get_unique.add_command(import_spotify_command.import_spotify)
get_unique.add_command(import_deezer_command.import_deezer)
get_unique.add_command(sync_spotify_command.sync_spotify)
get_unique.add_command(delete_command.delete_tracks)
get_unique.add_command(move_command.move_tracks)
get_unique.add_command(copy_command.copy_tracks)
