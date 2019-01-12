def show_items(station, get_inputs=False):
    # Attempting to make showing the prices reusable.  The inputs and displayed
    # prices could get out of sync during a trade session if the items in the
    # station changed.
    print("\n{:^14} {:^16} {:^10}".format('Items', 'Prices (B/S)', 'Supply'))
    print("{:^14} {:^16} {:^10}".format('¯' * 5, '¯' * 13, '¯' * 6))

    if get_inputs:
        commodity_choices = {}
        counter = 1
        valid_item_inputs = []
    for item in station['items']:
        item = station['items'][item]
        if get_inputs:
            commodity_choices[counter] = item.name
            valid_item_inputs.append(str(counter))
            counter += 1
        prices = f"{item.price_buy:<7}/{item.price_sell:>7}"
        print(f"{item.name:<14} {prices:^16} {item.units:^10}")
    if get_inputs:
        return commodity_choices, valid_item_inputs


def trade(UNI, player, station):
    # display commodities
    commodity_choices, valid_item_inputs = show_items(station, get_inputs=True)

    # do trading
    trade = ''
    while trade.upper() != 'Q':
        trade = input('Enter your choice (1-4 or Q)? ')
        player_ship = UNI.ships[player.ship_current]
        # find max cargo space available for trade
        cargo_used = sum([player_ship['cargo'][item] for item in player_ship['cargo']])
        available_holds = player_ship["holds_current"] - cargo_used
        print(f'\nYou have {player.wallet} credits and {available_holds} empty cargo holds.\n')
        if trade in valid_item_inputs:
            # get commodity data
            choice = station['items'][commodity_choices[int(trade)]]
            mode = input("Do you want to (B)uy or (S)ell?")
            if mode.upper() == 'B':
                wallet_max_buy = player.wallet // choice.price_sell
                max_buy = int(min(wallet_max_buy, available_holds))
                to_buy = input(f"We are selling up to {choice.units} of {choice.name}.  You have {available_holds} available holds.\nHow many do you want to buy? [{max_buy}] ")
                try:
                    to_buy_number = int(to_buy)
                except ValueError:
                    to_buy_number = 0
                if to_buy == '':
                    to_buy_number = max_buy
                if to_buy_number > 0 and to_buy_number <= max_buy:
                    if choice.name not in player_ship['cargo']:
                        player_ship['cargo'][choice.name] = to_buy_number
                    else:
                        player_ship['cargo'][choice.name] += to_buy_number

                    wallet_change = choice.price_sell * to_buy_number
                    player.wallet -= wallet_change
                    station['items'][choice.name].units -= to_buy_number
                    print(f'\n You bought {to_buy_number} units of {choice.name} for {wallet_change}.')
                    show_items(station)
                else:
                    print("\nThat's not a valid amount!\n")
                    show_items(station)

            elif mode.upper() == 'S':
                max_sell = player_ship['cargo'].get(choice.name, 0)
                to_sell = input(f"We are buying {choice.name} at {choice.price_sell} per unit.  You have {max_sell} available units.\nHow many do you want to sell? [{max_sell}] ")
                try:
                    to_sell_number = int(to_sell)
                except ValueError:
                    to_sell_number = 0
                if to_sell == '':
                    to_sell_number = max_sell
                elif to_sell_number > 0 and to_sell_number <= max_sell:
                    player_ship['cargo'][choice.name] -= to_sell_number
                    player.wallet += choice.price_buy * to_sell_number
                    wallet_change = choice.price_sell * to_sell_number
                    player.wallet -= wallet_change
                    station['items'][choice.name].units += to_sell_number
                    print(f'\n You sold {to_sell_number} units of {choice.name} for {wallet_change}.')
                    show_items(station)
                else:
                    print("\nThat's not a valid amount!\n")
                    show_items(station)

