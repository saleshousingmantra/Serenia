# Publishing schedule

`main` is the live site. `drafts` holds every page, including guides that are not live yet.

Live today: the three buying guides. The six locality guides go live one per day, starting 2026-11-22,
in the order listed in `scripts/schedule.json`.

## Publish the next guide
```bash
git checkout drafts && git pull
# add the next slug to "published" in scripts/schedule.json, commit on drafts
rm -rf /tmp/src && mkdir /tmp/src && git archive drafts | tar -x -C /tmp/src
git checkout main && git pull
python3 /tmp/src/scripts/apply-schedule.py /tmp/src .
git add -A && git commit -m "Publish guide: <title>" && git push origin main
```
The script removes links, cards and sitemap entries for guides that are not live yet, so the live site never links to a missing page.
