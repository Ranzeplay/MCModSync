import os
import shutil
import urllib.parse
import urllib.request

from colorist import red, green

import requests

from models.minecraft_mod import MinecraftMod

api_key = b"$2a$10$H/ywACoqS2KgoqFmEHLRMu5DfY4or0sVnc3JonT0EuGFHPIOWpkXS"


def download_curseforge_mod(mod: MinecraftMod):
    print(f'Downloading mod {mod["name"]} from CurseForge')

    headers = {
        'Accept': 'application/json',
        'x-api-key': api_key
    }

    queryParams = {
        'gameVersion': mod["version"],
    }

    candidate_versions = requests.get(f'https://api.curseforge.com/v1/mods/{mod["id"]}/files', headers=headers,
                                  params=queryParams).json()["data"]

    matched_versions = list(filter(lambda x: mod["loader"] in x["gameVersions"], candidate_versions))
    if len(matched_versions) > 0:
        version = matched_versions[0]

        download_url = version["downloadUrl"]
        filename = urllib.parse.unquote(download_url.split("/")[-1])
        filepath = os.path.join("downloads", filename)

        # urllib.request.urlretrieve(download_url, filepath, headers=headers)

        response = requests.get(download_url, headers=headers)
        with open(filepath, 'wb') as f:
            f.write(response.content)
            f.flush()

        for category in mod["categories"]:
            dir = os.path.join('downloads', category)
            if not os.path.exists(dir):
                os.mkdir(dir)
            shutil.copyfile(filepath, os.path.join(dir, filename))

        os.remove(filepath)

        green(f'Successfully downloaded {mod["name"]}')
    else:
        red(f'Project {mod["name"]} doesn\'t have the version for game version {mod["version"]}')
