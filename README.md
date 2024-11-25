# Mirror wars

I participated in the **Counterspell Hackathon** on November 23rd and 24th, 2024 for the first time. I was working with a team of three:  Vibhu Siddha, Tejas and I. 

## Theme of the hackathon
You are your own enemy.

## Game Details
We developed a game where the main character has to fight again his own shadow. This game has three levels. The way one wins the game is by killing the shadow and making it to the mirror. When you reach the three times, you WIN!

## Characterization
Player - Must kill the shadow by placing down a spike using "S". One spike per level. If the player touches the spike or touches the shadow, they die, and the game will need to be restarted. Pressing "F" when the shadow is still alive reverses the direction the shadow will go, and when "G" is pressed, it changes back to normal. 

Shadow - Unlike the player, the shadow is allowed to go through walls, and can only be killed by the spike. After the shadow is killed, you will be allowed to enter the mirror and move to the next level. The shadow will mimic all of the player's movements unless the player presses "F" on a mirror, for which the shadow will go the opposite direction as the player. 

Mirror - Allows player to progress through the game after the shadow is killed in the same level. The player may not pass through the mirror if the shadow is still alive. When the player interacts with the mirror and presses "F", the shadow's direction is reversed to that of the player's, and "G" sets it back to normal. 

## Tech stack

* Python 3
* PyGame
* LibreSprite for artwork (https://libresprite.github.io/)
* VSCode 

## How to play this game
* Fork this project
* run `pip install pygame` 
* Run the `main.py` from vscode

## Final game

![Game Preview](https://github.com/pranavganesh6/Hackclub-Counterspell-Hackathon/blob/main/character-assets/game.gif)



