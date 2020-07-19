/*
set @playerName = 'Mi% Lewis';
set @playerName2 = 'Chad Ochocinco';

select season, player, playerTeam, 
(select teamId from refData.nflTeams where season = teamYear and playerTeam = teamFantasyStats) as teamId,
playerPosition, min(week), max(week)
  from la_liga_data.pointsScored
where (player like concat('%',@playerName,'%') -- or player like concat('%',@playerName2,'%')
)
 and season >= 2007

group by 1,2,3,4,5
order by 2,1,5,6
;

select * from refData.players where playerName like concat('%',@playerName,'%') -- or playerName like concat('%',@playerName2,'%')
order by playerId, playerSeason;

*/

select a.*, playerMadden, playerId

from (select season, player, pos, teamId, minWeek, maxWeek from (
select season, player, 
playerPosition as pos ,
playerTeam as team, min(week) as minWeek, max(week) as maxWeek
 from la_liga_data.pointsScored
group by 1,2,3,4) a
left join refData.nflTeams on season = teamYear and teamFantasystats = team) a
left join refData.players on season = playerSeason and playerName = player 
and pos = playerPosition and playerTeam = teamId and playerFantasyStats = 1

where playerMadden is null
order by pos, season desc, teamId,  player;


/*
-- everything matches

update refData.players a
join (select a.*, playerId, playerMadden, playerNflStats
from (select season, player, pos, teamId, minWeek, maxWeek from (
select season, player, 
group_concat(distinct playerPosition) as pos ,
group_concat(distinct playerTeam) as team, min(week) as minWeek, max(week) as maxWeek
 from la_liga_data.pointsScored
-- and statPosition = 'RB'
group by 1,2) a
left join refData.nflTeams on season = teamYear and teamFantasystats = team) a
left join refData.players on season = playerSeason and player = playerName 
and pos = playerPosition and playerTeam = teamId

where playerMadden is not null

) b on season = playerSeason and playerName = player and pos = playerPosition and teamId = playerTeam

set a.playerFantasyStats = true;
*/

/*
-- matches on everything except periods
insert into refData.players

select distinct null, playerId, season, 0, 21, player, teamId, pos, false, false, false, false, true

from (select season, player, pos, teamId, minWeek, maxWeek from (
select season, player, 
group_concat(distinct playerPosition) as pos ,
group_concat(distinct playerTeam) as team, min(week) as minWeek, max(week) as maxWeek
 from la_liga_data.pointsScored
group by 1,2) a
left join refData.nflTeams on season = teamYear and teamFantasystats = team) a
left join refData.players on season = playerSeason and playerName != player and replace(playerName,'.','') = replace(player,'.','')
and pos = case when playerPosition in ('HB','FB') then 'RB' else playerPosition end and playerTeam = teamId

where playerMadden is not null;

*/


/*
-- match on players that changed teams
update refData.players a
join (
select season,player, playerPosition, startWeek, 
(select teamId from refData.nflTeams where season = teamYear and playerTeam = teamFantasyStats) as statTeam, 
(select teamId from refData.nflTeams where season = teamYear and firstTeam = teamFantasyStats) as firstTeam, 
if(max(week) = 
	(select max(week) 
		from la_liga_data.pointsScored a 
        where a.season = b.season and a.player = b.player and a.playerPosition = b.playerPosition
	),21,max(week)) as endWeek
from (
select b.*, 
@priorRow, concat_ws('-',season, player, playerPosition),
@startWeek := case when @priorRow != concat_ws('-',season, player, playerPosition) then 0
	when @priorTeam != playerTeam then @priorWeek + 1 else @startWeek end as startWeek,
@firstTeam := if (@priorRow != concat_ws('-',season, player, playerPosition),playerTeam,@firstTeam) as firstTeam,
@priorWeek := week,
@priorRow := concat_ws('-',season, player, playerPosition),
@priorTeam := playerTeam
from (
select season, week, player, playerPosition, group_concat(playerTeam) as playerTeam
from la_liga_data.pointsScored a
left join (
select season as countYear, week as countWeek, player as countPLayer, playerPosition as countPos, count(*)
from  la_liga_data.pointsScored
group by 1,2,3,4
having count(*) > 1
) b on countYear = season and countPlayer = player and countPos = playerPosition
where countYear is null -- and statPlayer in ('Mike Williams','Rod Smith')
group by player, playerPosition, season, week
order by player, playerPosition, season, week) b, (select @startWeek := 0, @firstTeam := '', @priorRow := '', @priorTeam := '', @priorWeek := 0) as t
) b 
group by 1,2,3,4,5,6) b
on season = playerSeason and player = playerName and b.playerPosition = a.playerPosition and startWeek = playerStartWeek and endWeek = playerEndWeek
	and b.statTeam = a.playerTeam
set playerFantasyStats = true;

    */
