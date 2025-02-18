SELECT COUNT(*) AS "Number of playbacks", title AS "Song title", name AS "Artist name"
FROM song s, artist a, stream sr
WHERE a.id = s.artist_id
AND s.id = sr.song_id
GROUP BY s.id
ORDER BY COUNT(*) DESC;
