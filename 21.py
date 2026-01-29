import os
import random
import time


def deck_generating():
    deck_36_card = [2, 3, 4, 6, 7, 8, 9, 10, 11] * 4
    random.shuffle(deck_36_card)
    return deck_36_card


def cards_stringing(cards):
    return str(cards).replace('2', 'J').replace('3', 'D').replace('4', 'K').replace('11', 'A').replace(', ', '] [')


def game_table(rnd, cards1, cards2, cards3, cards4, rnd_msg):
    table_width = 50
    table_high = 7
    left_sep = 5
    table = f'{" " * (int(table_width / 2 - 2))}Раунд {rnd}\n'
    table += f'{" " * table_high}/{"`" * table_width}/\n'
    table += f'{" " * (table_high - 1)}/{cards1.ljust(table_width - len(cards2), " ")}{cards2}/{" "}\n'
    for i in range(2, table_high - 1):
        table += f'{" " * (table_high - i)}/{" " * table_width}/{" " * i}\n'
    table += f'{" "}/{cards3.ljust(table_width - len(cards4), " ")}{cards4}/{" " * (table_high - 1)}\n'
    table += f'/{"." * table_width}/{" " * table_high}\n'
    table += f'{rnd_msg}'
    return table

    # return (f'{" " * (int(table_width / 2 - 2) + left_sep)}Раунд {rnd}\n'
    #         f'{" " * (3 + left_sep)}/{"`" * (table_width - 6)}\\\n'
    #         f'{" " * (2 + left_sep)}/{cards1.rjust((table_width - 4), " ")}\\\n'
    #         f'{" " * (1 + left_sep)}/{" " * (table_width - 2)}\\\n'
    #         f'{" " * left_sep}|{" " * table_width}|\n'
    #         f'{" " * (1 + left_sep)}\\{" " * (table_width - 2)}/\n'
    #         f'{" " * (2 + left_sep)}\\{cards2.ljust((table_width - 4), " ")}/\n'
    #         f'{" " * (3 + left_sep)}\\{"_" * (table_width - 6)}/\n'
    #         f'{rnd_msg}')


def cls():
    os.system('cls')


def game_print(rnd, dealer, player, round_msg):
    cls()
    print(game_table(rnd, cards_stringing(dealer), '', cards_stringing(player), '', round_msg))


def wrong_bet(choice, restriction_1, restriction_2):
    if choice < 1:
        cls()
        print('Минимальная ставка: 1.')
        time.sleep(3)
        return 1
    elif choice > restriction_1:
        cls()
        print(f'Ваша ставка превысила ваш баланс: {restriction_1}.')
        time.sleep(3)
        return 1
    elif choice > restriction_2:
        cls()
        print(f'Ваша ставка превысила банк: {restriction_2}.')
        time.sleep(3)
        return 1
    else:
        return 0


def additional_dealing(rnd_number, computer_hand, human_hand):
    # player
    for i in range(4):
        choice = int(input())
        # human choice
        if choice:
            human_hand.append(deck.pop())
        else:
            break
        game_print(rnd_number, '[ ]', human_hand,
                   f'Сумма очков: {sum(human_hand)}. Еще? 1 - Да, 0 - Нет')
        # stop dealing points
        if (sum(human_hand) == 22 and len(human_hand) == 2) or sum(human_hand) >= 21:
            return computer_hand, human_hand
    # dealer
    game_print(rnd_number, computer_hand, human_hand, f'Сумма очков банкира: {sum(computer_hand)}.')
    time.sleep(1)
    for j in range(4):
        if sum(computer_hand) < 17:
            computer_hand.append(deck.pop())
            game_print(rnd_number, computer_hand, human_hand, f'Сумма очков банкира: {sum(computer_hand)}.')
            time.sleep(1)
        else:
            break
    return computer_hand, human_hand


def additional_dealing(who):
    hand = dict(player=player_additional_dealing(), comp1=comp_additional_dealing(), comp2=None, comp3=None)
    return hand.get(who)


def player_additional_dealing():
    return 0


def comp_additional_dealing():
    return 0


def bust(hand):
    if (sum(hand) == 22 and len(hand) == 2) or (sum(hand) <= 21):
        return 0
    else:
        return 1


def player1_win_player2_lose(wallet_player1, wallet_player2, bet, msg):
    wallet_player1 += bet
    wallet_player2 -= bet
    cls()
    print(msg)
    time.sleep(3)
    return wallet_player1, wallet_player2


def reset(hand1, hand2):
    hand1.clear()
    hand2.clear()
    return 0


# points for bets
player_wallet = 200
bank = 200
# rounds counter
count = 1

# cards
player_hand = []  # comp1_hand = comp2_hand = comp3_hand = []
dealer_hand = []
massage = 'бебубэ'
# bet
player_bet = 0
player_hand_ready = 0

while bank and player_wallet:

    game_print(count, dealer_hand, player_hand, massage)

    if not bank:
        cls()
        print(f'Ваш баланс: {player_wallet}. Банк: {bank}.\nПоздравляю, Вы победитель! Банка больше нет!')
        break

    if not player_wallet:
        cls()
        print(f'Ваш баланс: {player_wallet}. Банк: {bank}.\nПоздравляю, Вы проиграли! Банк победил!')
        break

    if not max(len(player_hand), len(dealer_hand)):
        # deck generating
        deck = deck_generating()

        # first dealing
        player_hand.append(deck.pop())
        dealer_1_card = deck.pop()
        massage = f'Ваш баланс: {player_wallet}. Банк: {bank}.'
        continue

    if not player_bet:
        player_choice = int(input('Ваша ставка:'))
        if not wrong_bet(player_choice, player_wallet, bank):
            player_bet = player_choice
            massage = f'Сумма очков: {sum(player_hand)}. Еще? 1 - Да, 0 - Нет'
        continue

    if bust(player_hand):
        bank, player_wallet = player1_win_player2_lose(bank, player_wallet, player_bet,
                                                       f'Ваша сумма очков: {sum(player_hand)}. Перебор.')
        player_bet = reset(dealer_hand, player_hand)
        count += 1
        player_hand_ready = 0
        continue

    if bust(dealer_hand):
        player_wallet, bank = player1_win_player2_lose(player_wallet, bank, player_bet,
                                                       f'Ваша сумма очков: {sum(player_hand)}. Сумма очков дилера:{sum(dealer_hand)}. У дилера перебор.')
        player_bet = reset(dealer_hand, player_hand)
        count += 1
        player_hand_ready = 0
        continue

    if not player_hand_ready and len(player_hand) < 4:
        choice = int(input())
        if choice:
            player_hand.append(deck.pop())
            massage = f'Сумма очков: {sum(player_hand)}. Еще? 1 - Да, 0 - Нет'
            continue
        else:
            player_hand_ready = 1

    if len(dealer_hand) == 0:
        dealer_hand.append(dealer_1_card)
        massage = f'Сумма очков: {sum(dealer_hand)}.'
        print(1)
        continue
    if sum(dealer_hand) < 17 and len(dealer_hand) < 4:
        time.sleep(3)
        dealer_hand.append(deck.pop())
        massage = f'Сумма очков: {sum(dealer_hand)}.'
        print(1)
        continue

    if sum(player_hand) > sum(dealer_hand):
        player_wallet, bank = player1_win_player2_lose(player_wallet, bank, player_bet,
                                                       f'Ваша сумма очков: {sum(player_hand)}. Сумма очков дилера:{sum(dealer_hand)}. Вы выиграли этот раунд!')
    else:
        bank, player_wallet = player1_win_player2_lose(bank, player_wallet, player_bet,
                                                       f'Ваша сумма очков: {sum(player_hand)}. Сумма очков дилера: {sum(dealer_hand)}. Вы проиграли этот раунд.')
    player_bet = reset(dealer_hand, player_hand)
    count += 1
    player_hand_ready = 0