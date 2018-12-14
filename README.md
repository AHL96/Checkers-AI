# Machine-Learning-Final-Project
Using reinforcement learning to play checkers


## implementation

In checkers, only half of the board is used. So instead of using a 2D list to represent
the checker board we used a 1D list with 32 spots in it

how the player views it

|~|a|b|c|d|e|f|g|h|
|-|-|-|-|-|-|-|-|-|
|1| |0| |1| |2| |3
|2|4| |5| |6| |7|
|3| |8| |9| |10| |11
|4|12| |13| |14| |15|
|5| |16| |17| |18| |19
|6|20| |21| |22| |23|
|7| |24| |25| |26| |27
|8|28| |29| |30| |31|


how the computer views it

| | | | |
|-|-|-|-|
|0|1|2|3|
|4|5|6|7|
|8|9|10|11|
|12|13|14|15|
|16|17|18|19|
|20|21|22|23|
|24|25|26|27|
|28|29|30|31|


Moving

|row| even | odd |
|-|-|-|
|down right|5|4|
|down left|4|3|
|up right|-3|-4|
|up left|-4|-5|
