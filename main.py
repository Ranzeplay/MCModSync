import json
import os

from models.minecraft_mod import MinecraftMod
from platforms.curseforge_platform import download_curseforge_mod
from platforms.modrinth_platform import download_modrinth_mod

from colorist import yellow

# Load mod list file
mod_list_file = open('mod.json')
mod_list: list[MinecraftMod] = json.load(mod_list_file)

if not os.path.exists('downloads'):
    os.mkdir('downloads')

for mod in mod_list:
    if mod["provider"].lower() == "modrinth":
        download_modrinth_mod(mod)
    elif mod["provider"].lower() == "curseforge":
        download_curseforge_mod(mod)
    else:
        yellow(f'Unknown provider in mod {mod["name"]}')

mod_list_file.close()
