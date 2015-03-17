create view long_match_list as
	SELECT
		M_Id,
		P1 as player,
		P2 as opponent,
		(case when winner=P1 then 1 else 0 end) as wins
	FROM
		matches
	UNION
	SELECT
		M_Id,
		P2 as player,
		P1 as opponent,
		(case when winner=P2 then 1 else 0 end) as wins
	FROM
		matches
	ORDER BY
		M_Id;