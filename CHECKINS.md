Use this file to commit information clearly documenting your check-ins' content. If you want to store more information/details besides what's required for the check-ins that's fine too. Make sure that your TA has had a chance to sign off on your check-in each week (before the deadline); typically you should discuss your material with them before finalizing it here.

# Check-in 1 Report Items

## Provide a brief description of your planned DSL:

1. What is the high-level purpose of your DSL? What kind of users is it aimed at? What will it enable users to do?
   - Modular 2 person card game, allows a user to program a set of rules for the card game like Go Fish or BlackJack
   - Target users are card game enthusiasts or people who want to try creating multiplayer card games
   - Enables users to create 2 person custom card games with customized rules. Our vision for this project is to provide our users a virtual representation of a deck of cards and basic rules like “picking up a card”, “skip turn”, “shuffle cards”, and more to facilitate the user’s creativity.
2. What are the 2-3 rich features of your DSL? A rich feature should be more complex than a choice in a set (e.g., the ability to choose between colours for a title is not a “rich” feature). What customization will each feature enable? Which features can be combined to interact in useful or creative ways?
   - Loops: a user can create a game in which they can perform multiple actions in a single turn using the looping feature. For example, in Blackjack, a player can HIT as many times as the player wants using the loop whereas in Go Fish each player can perform a single action each turn.
   - Conditionals: User can create many conditions or scenarios which influence the mechanics of the game. For example, in regular BlackJack one game ending condition is sum of a users card going above 21. Users are able to create custom version of BlackJack where the conditional could be 25.
   - Mutable Variable: For storing variables related to the game
     - Eg. Storing the “bust” value of BlackJack as a variable so that the user has the option to change the value
3. Example snippets of your DSL that illustrate at least each rich feature, and any interesting interaction between those.

```
# Config
_CONFIG:
	use_jokers = NO
	number_of_decks = 1
	number_of_players = 2

# Looping
on_user_turn:
	# turn mechanics for playing Blackjack
	action = wait_for(Action::HIT, Action::STAY)
	loop if action is Action::HIT and player is _ALIVE:
		action = wait_for(Action::HIT, Action::STAY)

# Mutable Variables
blackjack_limit = 25

check_user_action:
	# Conditionals
	if cards_in_hand > blackjack_limit:
		game.end()
```

## Note any important changes/feedback from TA discussion.

- We need to prioritize ensuring the rich features are available for the user within the DSL
- Ensure that we are coding an interpreter and not a compiler (due to scope issues)
- User stories are important, but should not take precedent over the rich features

## Note any planned follow-up tasks or features still to design.

- Create a standard representation of our DSL and divide tasks.
- Design a state machine for the overall game logic: Pre-Game, In-Game and Post-Game states
