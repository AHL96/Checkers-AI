# Machine-Learning-Final-Project
Using reinforcement learning to play checkers


## implementation

In checkers, only half of the board is used. So instead of using a 2D list to represent
the checker board we used a 1D list with 32 spots in it

how the player views it

|~|a|b|c|d|e|f|g|h|
|-|-|-|-|-|-|-|-|-|
|1|_|0|_|1|_|2|_|3
|2|4|_|5|_|6|_|7|_
|3|_|8|_|9|_|10|_|11
|4|12|_|13|_|14|_|15|_
|5|_|16|_|17|_|18|_|19
|6|20|_|21|_|22|_|23|_
|7|_|24|_|25|_|26|_|27
|8|28|_|29|_|30|_|31|_


how the computer views it

|_|_|_|_|
|-|-|-|-|
|0|1|2|3|
|4|5|6|7|
|8|9|10|11|
|12|13|14|15|
|16|17|18|19|
|20|21|22|23|
|24|25|26|27|
|28|29|30|31|
