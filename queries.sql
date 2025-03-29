SELECT team, conference, games_won
FROM college_basketball
WHERE games_won > 20
ORDER BY games_won DESC LIMIT 5;

SELECT team, conference, field_goal_percentage, games_won
FROM college_basketball
WHERE field_goal_percentage > 50 AND games_won > 15;

SELECT team, offensive_efficiency
FROM college_basketball
ORDER BY offensive_efficiency DESC
LIMIT 5;

SELECT team, defensive_efficiency
FROM college_basketball
ORDER BY defensive_efficiency DESC
LIMIT 5;

