from django.db import migrations
from django.db.models import Count


def dedupe_likes_by_ip(apps, schema_editor):
    """Collapse Likes to one row per (post, ip_address).

    The old schema allowed one authenticated like per (post, user) AND one anonymous
    like per (post, ip_address). Both could exist for the same (post, ip_address) pair,
    which violates the new unconditional UniqueConstraint(post, ip_address). The oldest
    row in each group wins so the original "first liked at" timestamp is preserved.
    """
    Like = apps.get_model("likes", "Like")
    db_alias = schema_editor.connection.alias

    seen = set()
    ids_to_delete = []

    # Explicit ordering: Meta.ordering is ("-created_at",), which would keep the newest.
    rows = (
        Like.objects.using(db_alias)
        .order_by("post_id", "ip_address", "created_at", "id")
        .values_list("id", "post_id", "ip_address")
    )
    for like_id, post_id, ip_address in rows:
        key = (post_id, ip_address)
        if key in seen:
            ids_to_delete.append(like_id)
        else:
            seen.add(key)

    for start in range(0, len(ids_to_delete), 500):
        chunk = ids_to_delete[start : start + 500]
        Like.objects.using(db_alias).filter(id__in=chunk).delete()

    print(f"  dedupe_likes_by_ip: deleted {len(ids_to_delete)} duplicate like(s)")

    remaining = (
        Like.objects.using(db_alias)
        .values("post_id", "ip_address")
        .annotate(n=Count("id"))
        .filter(n__gt=1)
        .count()
    )
    if remaining:
        raise RuntimeError(
            f"dedupe_likes_by_ip left {remaining} duplicate (post, ip_address) group(s)"
        )


class Migration(migrations.Migration):
    dependencies = [
        ("likes", "0003_alter_like_options"),
    ]

    operations = [
        # Deleted rows cannot be restored, so the reverse is a no-op. It still has to be
        # set, otherwise the migration is irreversible and blocks any rollback.
        migrations.RunPython(dedupe_likes_by_ip, migrations.RunPython.noop),
    ]
