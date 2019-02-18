select 
usage_type,
datetime(lastime/1000, 'UNIXEPOCH', 'localtime') as lasttimeactive,
timeactive as time_Active_in_msecs,
timeactive/1000 as timeactive_in_secs,
package,
CASE types
     WHEN '1' THEN 'MOVE_TO_FOREGROUND'
     WHEN '2' THEN 'MOVE_TO_BACKGROUND'
     WHEN '5' THEN 'CONFIGURATION_CHANGE'
	 WHEN '7' THEN 'USER_INTERACTION'
	 WHEN '8' THEN 'SHORTCUT_INVOCATION'
     ELSE types
END types,
classs,
source,
fullatt
from data
order by lasttimeactive