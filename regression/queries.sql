/*select draftYear, team, player, position, playerTeam, draftRound, draftPick, pickValue, points - replacePoints  as por,
(points - replacePoints) - pickValue as keeperValue
from la_liga_data.keepers
left join refData.pickValue pick1 on draftPick = pick1.pickNumber
left join (select statYear, statPlayer, statPosition, sum(totalPoints) as points
from scrapped_data.playerStats
group by 1,2,3) b on statYear = draftYear and statPlayer = player and statPosition = position
left join analysis.replacementValue on replaceYear = draftYear and replacePosition = position
where draftYear < 2018 and team = 'JJ Burke'
order by keeperValue desc;*/


select team, sum((ifnull(points,0) - replacePoints) - pickValue) as keeperValue,
substring_index(group_concat(concat(draftYear,'_',draftPick,'_',replace(player,'_',"'"),'_',ifnull(points,0))
	order by (ifnull(points,0) - replacePoints) - pickValue desc separator '|'),'|',1) as bestKeeper, 
substring_index(group_concat(concat(draftYear,'_',draftPick,'_',replace(player,'_',"'"),'_',ifnull(points,0))
	 order by (ifnull(points,0) - replacePoints) - pickValue asc separator '|'),'|',1) as worstKeeper
from la_liga_data.keepers
left join refData.pickValue pick1 on draftPick = pick1.pickNumber
left join (select statYear, statPlayer, statPosition, sum(totalPoints) as points
from scrapped_data.playerStats
group by 1,2,3) b on statYear = draftYear and statPlayer = player and statPosition = position
left join analysis.replacementValue on replaceYear = draftYear and replacePosition = position
where draftYear < 2018
group by 1
order by 2 desc;



select draftYear, selectingTeam,player, preRank, draftPick, actualPick,
sum(greatest(pick1.actualPickValue,0)) as picksCapital,
sum(greatest(ifnull(pick2.actualPickValue-pick1.actualPickValue,0),0)) as keeperCapital,
sum(greatest(pick1.actualPickValue,0)) +
sum(greatest(ifnull(pick2.actualPickValue-pick1.actualPickValue,0),0)) as draftCapital

from (select a.draftYear,
a.draftRound, 
a.draftPick,
a.selectingTeam,
a.player,
a.playerPosition,
a.playerTeam,
if(b.draftYear is null,'N','Y') as keeper,
preRank,
a.draftPick +
(select count(*)
from (
select draftYear, draftPick, player,
keeperPick, preRank,
@row := if(@label = concat(draftYear,'-',draftPick),
@row + 1,draftPick) as addPick,
@label := concat(draftYear,'-',draftPick)
from (
select d.draftYear, d.draftPick, d.player,
e.draftPick as keeperPick, preRank
from la_liga_data.draftData d
join 
(select e.*, preRank from la_liga_data.keepers e
join scrapped_data.preRanks f on preYear = e.draftYear and prePlayer = e.player and prePosition = position) e
on e.draftYear = d.draftyear and e.draftPick > d.draftPick
order by d.draftYear, d.draftPick, preRank) d
join (select @row := 0, @label := cast('' as char)) t) d
where addPick >= preRank and d.draftYear = a.draftYear and d.draftPick = a.draftPick
) as actualPick


from la_liga_data.draftData a

left join la_liga_data.keepers b on a.draftYear = b.draftYear and a.player = b.player and a.playerPosition = b.position
left join scrapped_data.preRanks c on preYear = b.draftYear and prePlayer = b.player and prePosition = position
where a.draftYear = 2013 and selectingTeam = 'Chris Curtin'
) b
left join 
refData.pickValue pick1 on actualPick = pick1.pickNumber
left join 
refData.pickValue pick2 on preRank = pick2.pickNumber
group by 1,2 ,3,4,5,6
order by keeperCapital desc
