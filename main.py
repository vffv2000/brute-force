import json
import time

import requests
from art import tprint

import itertools
from eth_account import Account

def hello_message():
    tprint("vffv2000", font="rnd-medium")
    print("Contact me for custom script development")
    print("""Telegramm -  @vffv2000
    Discord - vffv2000/vffv2000#6942 
    Fiverr - @valentin_vffv 
    Donations - 0x943778dd179f13Bc5C036Bb4227Bf6e711dFA4F6""")
    print('''----------------------- Start -------------------------------
    ''')




def generate_word_combinations(words, num_words, start_position):
    combination = itertools.combinations(words, num_words)
    for _ in range(start_position):
        next(combination)
    yield from combination

def save_position(position):
    with open('position.txt', 'w') as file:
        file.write(str(position))

def load_position():
    try:
        with open('position.txt', 'r') as file:
            position = int(file.read())
            return position
    except FileNotFoundError:
        return 0

def save_values_to_txt(value1, value2, value3, value4):
    content = f"{value1} {value2} {value3} {value4}\n"
    with open('wallets.txt', 'a') as file:
        file.write(content)

def main():
    # Включение функций Mnemonic
    Account.enable_unaudited_hdwallet_features()
    filename = 'word_list.txt'  # Укажите имя вашего файла
    num_words = 12  # Количество слов в каждой комбинации

    with open(filename, 'r') as file:
        words = file.read().splitlines()

    position = load_position()
    combinations_generator = generate_word_combinations(words, num_words, position)

    i = 0
    for combination in combinations_generator:
        combination_str = ' '.join(combination)

        try:
            private_key = Account.from_mnemonic(combination_str)
            print(combination_str, private_key.address, private_key._private_key.hex())
            balance = check_eth_balance(private_key.address)
            print(balance)
            if balance != 0.0:
                save_values_to_txt(balance, private_key.address, private_key._private_key.hex(), combination_str)
        except:
            print("wallet clear")

        i += 1
        save_position(position + i)



def check_eth_balance(address):
    rpc_url = "https://rpc.ankr.com/eth"

    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [address, "latest"],
        "id": 1
    }

    response = requests.post(rpc_url, json=payload)
    result = json.loads(response.text)

    if "result" in result:
        balance_wei = int(result["result"], 16)
        balance_eth = balance_wei / 10 ** 18
        return balance_eth
    elif "error" in result:
        error_message = result["error"]["message"]
        raise ValueError(f"Ошибка при запросе баланса Ethereum: {error_message}")
    else:
        raise ValueError("Не удалось получить ответ от JSON-RPC сервера")

if __name__ == '__main__':
    main()

