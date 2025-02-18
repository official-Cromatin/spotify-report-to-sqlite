SELECT time(SUM(duration) / 1000, 'unixepoch') AS "Overall duration", title AS "Song title", name AS "Artist name"
FROM song s, artist a, stream sr
WHERE a.id = s.artist_id
AND s.id = sr.song_id
GROUP BY s.id
ORDER BY time(SUM(duration) / 1000, 'unixepoch') DESC;
