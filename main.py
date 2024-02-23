import json

import init_django_orm  # noqa: F401

from db.models import Race, Skill, Player, Guild


def main() -> None:
    with open("players.json") as config_file:
        players = json.load(config_file)

    for nickname, player in players.items():
        race = player.get("race")
        skills = player.get("race").pop("skills")
        race_object, race_created = Race.objects.get_or_create(**race)

        if race_created and skills:
            for skill in skills:
                skill["race"] = race_object
                Skill.objects.get_or_create(**skill)

        guild = player.get("guild")
        guild_object, _ = Guild.objects.get_or_create(
            **guild
        ) if guild is not None else (None, None)

        Player.objects.get_or_create(
            nickname=nickname,
            email=player.get("email"),
            bio=player.get("bio"),
            race=race_object,
            guild=guild_object,
        )


if __name__ == "__main__":
    main()
