SELECT time(SUM(duration) / 1000, 'unixepoch') AS "Overall duration", title AS "Song title"
FROM song s, artist a, stream sr
WHERE a.id = s.artist_id
AND s.id = sr.song_id
AND a.name = "<ARTIST NAME HERE>"
GROUP BY s.id
ORDER BY time(SUM(duration) / 1000, 'unixepoch') DESC;
