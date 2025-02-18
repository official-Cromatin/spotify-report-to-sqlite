SELECT name AS "Artist name", time(SUM(duration) / 1000, 'unixepoch') AS "Overall duration"
FROM song s
JOIN artist a ON s.artist_id = a.id
JOIN stream sr ON sr.song_id = s.id
GROUP BY a.id
ORDER BY time(SUM(duration) / 1000, 'unixepoch') DESC;
