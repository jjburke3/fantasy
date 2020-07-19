/*
set @playerName = 'Jeff Wilson';


select statYear, statPlayer, statTeam, 
(select teamId from refData.nflTeams where statYear = teamYear and statTeam = teamNflStats) as teamId,
statPosition, min(statWeek), max(statWeek)
  from scrapped_data.playerStats
where (statPlayer like concat('%',@playerName,'%') -- or statPlayer like '%Buck Allen%'
)
 and statYear >= 2007

group by 1,2,3,4,5
order by 2,1,5,6
;

select * from refData.players where playerName like concat('%',@playerName,'%') -- or playerName like '%Buck Allen%'
order by playerId, playerSeason;

*/

select a.*, playerMadden, playerId

from (select statYear, statPLayer, pos, teamId, minWeek, maxWeek from (
select statYear, statPlayer, 
statPosition as pos ,
statTeam as team, min(statWeek) as minWeek, max(statWeek) as maxWeek
 from scrapped_data.playerStats where statYear >= 2007
group by 1,2,3,4) a
left join refData.nflTeams on statYear = teamYear and teamNflstats = team) a
left join refData.players on statYear = playerSeason and playerName = statPLayer 
and pos = playerPosition and playerTeam = teamId

where playerMadden is null
order by pos, statYear desc, teamId,  statPlayer;


/*
-- everything matches

update refData.players
join (select a.*, playerId, playerMadden, playerNflStats
from (select statYear, statPLayer, pos, teamId, minWeek, maxWeek from (
select statYear, statPlayer, 
group_concat(distinct statPosition) as pos ,
group_concat(distinct statTeam) as team, min(statWeek) as minWeek, max(statWeek) as maxWeek
 from scrapped_data.playerStats where statYear >= 2007
-- and statPosition = 'RB'
group by 1,2) a
left join refData.nflTeams on statYear = teamYear and teamNflstats = team) a
left join refData.players on statYear = playerSeason and playerName = statPLayer 
and pos = playerPosition and playerTeam = teamId

where playerMadden is not null;

) b on statYear = playerSeason and playerName = statPlayer and pos = playerPosition and teamId = playerTeam

set a.playerNflStats = true;
*/

/*
-- hb/fb to rb switch
insert into refData.players

select null, playerId, statYear, 0, 21, statPlayer, teamId, pos, false, false, false, true, false

from (select statYear, statPLayer, pos, teamId, minWeek, maxWeek from (
select statYear, statPlayer, 
group_concat(distinct statPosition) as pos ,
group_concat(distinct statTeam) as team, min(statWeek) as minWeek, max(statWeek) as maxWeek
 from scrapped_data.playerStats where statYear >= 2007
and statPosition = 'RB'
group by 1,2) a
left join refData.nflTeams on statYear = teamYear and teamNflstats = team) a
left join refData.players on statYear = playerSeason and playerName = statPLayer 
and pos = case when playerPosition in ('HB','FB') then 'RB' else playerPosition end and playerTeam = teamId

where playerMadden is not null;
*/

/*
-- matches on everything except periods
insert into refData.players

select null, playerId, statYear, 0, 21, statPlayer, teamId, pos, false, false, false, true, false

from (select statYear, statPLayer, pos, teamId, minWeek, maxWeek from (
select statYear, statPlayer, 
group_concat(distinct statPosition) as pos ,
group_concat(distinct statTeam) as team, min(statWeek) as minWeek, max(statWeek) as maxWeek
 from scrapped_data.playerStats where statYear >= 2007
group by 1,2) a
left join refData.nflTeams on statYear = teamYear and teamNflstats = team) a
left join refData.players on statYear = playerSeason and playerName != statPLayer and replace(playerName,'.','') = replace(statPLayer,'.','')
and pos = case when playerPosition in ('HB','FB') then 'RB' else playerPosition end and playerTeam = teamId

where playerMadden is not null;

*/


/*
insert players that started with same team but moved around
insert into refData.players
select null, a.playerId, statYear, startWeek, endWeek, statPlayer, statTeam, statPosition, 
false,false,false,true,false
from (
select statYear,statPlayer, statPosition, startWeek, 
(select teamId from refData.nflTeams where statYear = teamYear and statTeam = teamNflStats) as statTeam, 
(select teamId from refData.nflTeams where statYear = teamYear and firstTeam = teamNflStats) as firstTeam, 
if(max(statWeek) = 
	(select max(statWeek) 
		from scrapped_data.playerStats a 
        where a.statYear = b.statYear and a.statPlayer = b.statPlayer and a.statPosition = b.statPosition
	),21,max(statWeek)) as endWeek
from (
select b.*, 
@priorRow, concat_ws('-',statYear, statPlayer, statPosition),
@startWeek := case when @priorRow != concat_ws('-',statYear, statPlayer, statPosition) then 0
	when @priorTeam != statTeam then @priorWeek + 1 else @startWeek end as startWeek,
@firstTeam := if (@priorRow != concat_ws('-',statYear, statPlayer, statPosition),statTeam,@firstTeam) as firstTeam,
@priorWeek := statWeek,
@priorRow := concat_ws('-',statYear, statPlayer, statPosition),
@priorTeam := statTeam
from (
select statYear, statWeek, statPlayer, statPosition, group_concat(statTeam) as statTeam
from scrapped_data.playerStats a
left join (
select statYear as countYear, statWeek as countWeek, statPlayer as countPLayer, statPosition as countPos, count(*)
from  scrapped_data.playerStats
group by 1,2,3,4
having count(*) > 1
) b on countYear = statYear and countPlayer = statPlayer and countPos = statPosition
where statYear >= 2007 and countYear is null -- and statPlayer in ('Mike Williams','Rod Smith')
group by statPlayer, statPosition, statYear, statWeek
order by statPlayer, statPosition, statYear, statWeek) b, (select @startWeek := 0, @firstTeam := '', @priorRow := '', @priorTeam := '', @priorWeek := 0) as t
) b 
group by 1,2,3,4,5,6) b
join (select distinct playerId, playerName, playerSeason, playerPosition, playerTeam
		from refData.players 
        where playerStartWeek = 0 and playerEndWeek = 21 and playerMadden = true
	) a on a.playerName = statPlayer and statYear = a.playerSeason and a.playerTeam = firstTeam
	and statPosition = case when a.playerPosition in ('HB','FB') then 'RB' else a.playerPosition end
left join (select distinct playerId, playerName, playerSeason, playerPosition, playerTeam
	from refData.players where playerNflStats = true) c on c.playerName = statPlayer and c.playerSeason = statYear
    and c.playerPosition = statPosition and c.playerTeam = statTeam
where c.playerName is null

    */
    
/*
-- same name and position but different year, no duplicates in name, no same player multiple names


insert into refData.players
select null, a.playerId, statYear, startWeek, endWeek, statPlayer, statTeam, statPosition, 
false,false,false,true,false
from (
select statYear,statPlayer, statPosition, startWeek, 
(select teamId from refData.nflTeams where statYear = teamYear and statTeam = teamNflStats) as statTeam, 
(select teamId from refData.nflTeams where statYear = teamYear and firstTeam = teamNflStats) as firstTeam, 
if(max(statWeek) = 
	(select max(statWeek) 
		from scrapped_data.playerStats a 
        where a.statYear = b.statYear and a.statPlayer = b.statPlayer and a.statPosition = b.statPosition
	),21,max(statWeek)) as endWeek
from (
select b.*, 
@priorRow, concat_ws('-',statYear, statPlayer, statPosition),
@startWeek := case when @priorRow != concat_ws('-',statYear, statPlayer, statPosition) then 0
	when @priorTeam != statTeam then @priorWeek + 1 else @startWeek end as startWeek,
@firstTeam := if (@priorRow != concat_ws('-',statYear, statPlayer, statPosition),statTeam,@firstTeam) as firstTeam,
@priorWeek := statWeek,
@priorRow := concat_ws('-',statYear, statPlayer, statPosition),
@priorTeam := statTeam
from (
select statYear, statWeek, statPlayer, statPosition, group_concat(statTeam) as statTeam
from scrapped_data.playerStats a
left join (
select statYear as countYear, statWeek as countWeek, statPlayer as countPLayer, statPosition as countPos, count(*)
from  scrapped_data.playerStats
group by 1,2,3,4
having count(*) > 1
) b on countYear = statYear and countPlayer = statPlayer and countPos = statPosition
where statYear >= 2007 and countYear is null -- and statPlayer in ('Mike Williams','Rod Smith')
group by statPlayer, statPosition, statYear, statWeek
order by statPlayer, statPosition, statYear, statWeek) b, (select @startWeek := 0, @firstTeam := '', @priorRow := '', @priorTeam := '', @priorWeek := 0) as t
) b 
group by 1,2,3,4,5,6) b
join (select playerId, group_concat(distinct playerName) as playerName1, 
group_concat(distinct case when playerPosition in ('HB','FB') then 'RB' else playerPosition end) as playerPosition
		from refData.players 
        group by playerId
        having count(distinct(playerName)) = 1 and 
			playerName1 not in (select playerName from refData.players group by playerName having count(distinct(playerId)) > 1)
	) a on a.playerName1 = statPlayer
	and statPosition = a.playerPosition
left join (select distinct playerId, playerName, playerSeason, playerPosition, playerTeam
	from refData.players where playerNflStats = true) c on c.playerName = statPlayer and c.playerSeason = statYear
    and c.playerPosition = statPosition and c.playerTeam = statTeam
where c.playerName is null
*/