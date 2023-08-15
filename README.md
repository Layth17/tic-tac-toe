# tic-tac-toe: *extended*
Applying RL to play tic-tac-toe
> This work builds upon this source [here](https://towardsdatascience.com/reinforcement-learning-implement-tictactoe-189582bea542)

> note: this is no longer an install-and-play product because it was *extended*. I should have branched out in retrospect :)

### RL formula
![formula](./images/formula.png)

### TODO:
- [x] Added player 2 policy
- [x] Improved human vs computer 
- [x] Improved logging
- [x] Performed action space analysis
- [x] Add the ability to train on top of previous policies
- [ ] Make above ^ more user-friendly 
- [ ] Pass command-line arguments
- [ ] Extend to 4x4? -- this endeavour has revealed many problems 
- [ ] Implement other variants?

-------------------------------
### The Ultimate Draw 3x3:
> *note: this is based on policy 582023_19237*

<div class="image-container">
  <img class="fade" src="./images/0.png" style="width:40%;height:40%;"> <img class="fade" src="./images/1.png" style="width:40%;height:40%;"> 
  <img class="fade" src="./images/2.png" style="width:40%;height:40%;"> <img class="fade" src="./images/3.png" style="width:40%;height:40%;">  
  <img class="fade" src="./images/4.png" style="width:40%;height:40%;"> <img class="fade" src="./images/5.png" style="width:40%;height:40%;">  
  <img class="fade" src="./images/6.png" style="width:40%;height:40%;"> <img class="fade" src="./images/7.png" style="width:40%;height:40%;">
  <img class="fade" src="./images/8.png" style="width:40%;height:40%;"> <img class="fade" src="./images/9.png" style="width:40%;height:40%;">
</div>

### Most Played Endings:
> *note: information is extracted from ./analysis_3by3/games.json*

``` text
This position was played 1549 times!
  p1: x  p2: o
   
   x|o|x
   -+-+-
   o|x|x
   -+-+-
   o|x|o
```

``` text
This position was played 1490 times!
  p1: x  p2: o
   
   x|x|o
   -+-+-
   o|x|x
   -+-+-
   x|o|o
```

``` text
This position was played 1483 times!
  p1: x  p2: o
   
   x|o|x
   -+-+-
   x|x|o
   -+-+-
   o|x|o
```


