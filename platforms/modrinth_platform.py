import os.path
import shutil
import urllib.request
import urllib.parse

from colorist import red, green

import requests

from models.minecraft_mod import MinecraftMod


def download_modrinth_mod(mod: MinecraftMod):
    print(f'Downloading mod {mod["name"]} from Modrinth')
    versions_response = requests.get(f'https://api.modrinth.com/v2/project/{mod["id"]}/version')
    if versions_response.ok:
        versions: list = versions_response.json()

        matched_versions = list(
            filter(lambda x: mod["version"] in x["game_versions"] and mod["loader"] in x["loaders"], versions))
        if len(matched_versions) > 0:
            version = matched_versions[0]

            download_url = version["files"][0]["url"]
            filename = urllib.parse.unquote(download_url.split("/")[-1])
            filepath = os.path.join("downloads", filename)

            urllib.request.urlretrieve(download_url, filepath)

            for category in mod["categories"]:
                dir = os.path.join('downloads', category)
                if not os.path.exists(dir):
                    os.mkdir(dir)
                shutil.copyfile(filepath, os.path.join(dir, filename))

            os.remove(filepath)

            green(f'Successfully downloaded {mod["name"]}')
        else:
            red(f'Project {mod["name"]} doesn\'t have the version for game version {mod["version"]}')
    else:
        red(f'Project {mod["name"]} not found')
