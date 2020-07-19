/*
insert into refData.players

select null, null, season, 0, 21, player_name, 
teamId, pos, true, false, false, false, false
 from madden_ratings.playerRatings
 join refData.nflTeams on season = teamYear and team = teamMadden 
 where season = 2019;
 */
 
 -- dup names
 set @season = 2018;
select player_name, count(case when season = @season-1 then 1 end) as countPrior, count(case when season = @season then 1 end) as countCurrent,
group_concat(concat_ws('-',team, pos, season))
from madden_ratings.playerRatings
where season in (@season-1,@season)
group by 1
having countPrior > 1 or countCurrent > 1;



/*
set @season = 2019;
-- update same name, same team, same position
update refData.players a
join (select playerId, playerName, playerSeason, playerTeam, playerPosition
from refData.players
where playerId is not null) b on a.playerName = b.playerName and a.playerSeason = b.playerSeason + 1
and a.playerTeam = b.playerTeam and a.playerPosition = b.playerPosition
set a.playerId = b.playerId
where a.playerId is null and a.playerSeason = @season;


-- update same name, same team, same position, 2 years prior
update refData.players a
join (select playerId, playerName, playerSeason, playerTeam, playerPosition
from refData.players
where playerId is not null) b on a.playerName = b.playerName and a.playerSeason = b.playerSeason + 2
and a.playerTeam = b.playerTeam and a.playerPosition = b.playerPosition
set a.playerId = b.playerId
where a.playerId is null and a.playerSeason = @season;

-- update same name, different team, same position group, no double names in either year
update refData.players a
join (select playerId, playerName, playerSeason, playerTeam, playerPosition
from refData.players
where playerId is not null) b on a.playerName = b.playerName and a.playerSeason = b.playerSeason + 1
and 
	case when a.playerPosition in ('RT','RG','C','LG','LT') then 'OT'
		when a.playerPosition in ('RE','LE','DT','ROLB','LOLB','MLB') then 'DL'
        when a.playerPosition in ('FS','SS','CB') then 'DB'
        when a.playerPosition = 'FB' then 'HB'
        else a.playerPosition end
    = 
    case when b.playerPosition in ('RT','RG','C','LG','LT') then 'OT'
		when b.playerPosition in ('RE','LE','DT','ROLB','LOLB','MLB') then 'DL'
        when b.playerPosition in ('FS','SS','CB') then 'DB'
        when b.playerPosition = 'FB' then 'HB'
        else b.playerPosition end
set a.playerId = b.playerId
where a.playerId is null and a.playerSeason = @season
and a.playerName not in (
select player_name from (select player_name, count(case when season = @season - 1 then 1 end) as countPrior, count(case when season = @season then 1 end) as countCurrent
from madden_ratings.playerRatings
where season in (@season-1,@season)
group by 1
having countPrior > 1 or countCurrent > 1)b );

*/

-- references for position swaps, or double names

select a.id, a.playerId, a.playerSeason, a.playerName, a.playerPosition,
(select teamMadden from refData.nflTeams where a.playerSeason = teamYear and a.playerTeam = teamId) as playerTeamA,
b.playerId, b.playerSeason, b.playerName, b.playerPosition,
(select teamMadden from refData.nflTeams where b.playerSeason = teamYear and b.playerTeam = teamId) as playerTeamA
 from refData.players a
join (select playerId, playerSeason, playerName, playerTeam, playerPosition
from refData.players
where playerId is not null) b on a.playerName = b.playerName and a.playerSeason > b.playerSeason 
 where a.playerId is null;
 /*
 select * from refData.players where playerName in (

 ) 
 order by playerName, playerSeason;
 */
 
 
-- reference for suffixs or initials
set @season = 2019;
select id, playerId, playerSeason, playerName, playerTeam, playerPosition,concat('%',substring_index(a.playerName,' ',-1),'%'),
(select count(*) from refData.players b where b.playerName like concat('%',substring_index(a.playerName,' ',-1),'%') and 
case when a.playerSeason = @season then b.playerSeason < @season else b.playerSeason = @season end) as matches
from refData.players a where   (playerId is null or 
(playerSeason = @season - 1 and 
	playerId not in (select ifnull(playerID,0) from refData.players where playerSeason = @season)
)) and 
 (playerName like '%jr' or playerName like '%sr' or playerName like '% II' or playerName like '% III' or playerName like '% IV' or playerName like '%.%'
	or playerName like '%\_%' or playerName like '% V');
select * from refData.players where playerName like 'richie james%' and playerSeason <= @season order by playerName, playerSeason ;

 -- add ids for all new players
/*
set @maxId = (select max(playerId) from refData.players);
update refData.players
set playerId = (@maxId := @maxId + 1)
where playerId is null;
*/