import requests
import json
from web3 import Web3
import config

lista_axie = []
lista_price = []
lista_img = []
tomala = []


def compra_axie(ax):
    amem = 1
    data = {
        "operation": "GetAxieDetail",
        "variables": {
            "axieId": "{}".format(ax)
        },
        "query": "query GetAxieDetail($axieId: ID!) {\n  axie(axieId: $axieId) {\n    ...AxieDetail\n    __typename\n  }\n}\n\nfragment AxieDetail on Axie {\n  id\n  image\n  class\n  chain\n  name\n  genes\n  owner\n  birthDate\n  bodyShape\n  class\n  sireId\n  sireClass\n  matronId\n  matronClass\n  stage\n  title\n  breedCount\n  level\n  figure {\n    atlas\n    model\n    image\n    __typename\n  }\n  parts {\n    ...AxiePart\n    __typename\n  }\n  stats {\n    ...AxieStats\n    __typename\n  }\n  auction {\n    ...AxieAuction\n    __typename\n  }\n  ownerProfile {\n    name\n    __typename\n  }\n  battleInfo {\n    ...AxieBattleInfo\n    __typename\n  }\n  children {\n    id\n    name\n    class\n    image\n    title\n    stage\n    __typename\n  }\n  __typename\n}\n\nfragment AxieBattleInfo on AxieBattleInfo {\n  banned\n  banUntil\n  level\n  __typename\n}\n\nfragment AxiePart on AxiePart {\n  id\n  name\n  class\n  type\n  specialGenes\n  stage\n  abilities {\n    ...AxieCardAbility\n    __typename\n  }\n  __typename\n}\n\nfragment AxieCardAbility on AxieCardAbility {\n  id\n  name\n  attack\n  defense\n  energy\n  description\n  backgroundUrl\n  effectIconUrl\n  __typename\n}\n\nfragment AxieStats on AxieStats {\n  hp\n  speed\n  skill\n  morale\n  __typename\n}\n\nfragment AxieAuction on Auction {\n  startingPrice\n  endingPrice\n  startingTimestamp\n  endingTimestamp\n  duration\n  timeLeft\n  currentPrice\n  currentPriceUSD\n  suggestedPrice\n  seller\n  listingIndex\n  state\n  __typename\n}\n"
    }
    while (amem == 1):
        try:
            aa = requests.post('https://graphql-gateway.axieinfinity.com/graphql', json=data)
            bb = aa.json()
            seller = bb['data']['axie']['auction']['seller']
            listing_inx = bb['data']['axie']['auction']['listingIndex']
            listing_stat = bb['data']['axie']['auction']['state']
            price = bb['data']['axie']['auction']['currentPrice']
            
            
            seller_addrs = Web3.toChecksumAddress(seller)
            token_adrss = Web3.toChecksumAddress('0xc99a6a985ed2cac1ef41640596c5a5f9f4e19ef5')
            price = int(price)
            listingIndex = int(listing_inx)
            listingState = int(listing_stat)

            headers = {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}
            web3txn = Web3(Web3.HTTPProvider('https://proxy.roninchain.com/free-gas-rpc',
                                             request_kwargs={"headers": headers}))
            web3 = Web3(Web3.HTTPProvider('https://api.roninchain.com/rpc',
                                          request_kwargs={"headers": headers}))
            with open("market_abi.json") as f:
                restake_abi = json.load(f)
            contract = web3.eth.contract(address=Web3.toChecksumAddress(
                "0x213073989821f738a7ba3520c3d31a1f9ad31bbd"), abi=restake_abi)
            _to = Web3.toChecksumAddress(config.TO_ACCOUNT_ADDRESS)  # To address
            _from = Web3.toChecksumAddress(config.FROM_ACCOUNT_ADDRESS)  # From address
            nonce = web3.eth.get_transaction_count(_from)
            transfer_txn = contract.functions.settleAuction(seller_addrs, token_adrss, price, listingIndex,
                                                            listingState,
                                                            Web3.toChecksumAddress(
                                                                '0x0000000000000000000000000000000000000000')).buildTransaction(
                {
                    'chainId': 2020,
                    'gas': 3000000,
                    'gasPrice': web3txn.toWei('1500', 'gwei'),
                    'nonce': nonce, })
            signed_txn = web3txn.eth.account.sign_transaction(transfer_txn,
                                                              private_key=bytearray.fromhex(config.FROM_PK.replace("0x",
                                                                                                                   "")))  # sender's private key
            rawTxn = signed_txn.rawTransaction
            tx_hash = web3txn.eth.send_raw_transaction(rawTxn)
            web3txn.eth.wait_for_transaction_receipt(tx_hash)
            print(f'Check: https://explorer.roninchain.com/tx/{web3.toHex(web3.keccak(rawTxn))}')
            amem = 2
        except:
            print('ainda não')

def selectd_axie(axie_id):
  golden = []
  data = {
    "operation": "GetAxieDetail",
    "variables": {
      "axieId": axie_id
    },
    "query": "query GetAxieDetail($axieId: ID!) {\n  axie(axieId: $axieId) {\n    ...AxieDetail\n    __typename\n  }\n}\n\nfragment AxieDetail on Axie {\n  id\n  image\n  class\n  chain\n  name\n  genes\n  owner\n  birthDate\n  bodyShape\n  class\n  sireId\n  sireClass\n  matronId\n  matronClass\n  stage\n  title\n  breedCount\n  level\n  figure {\n    atlas\n    model\n    image\n    __typename\n  }\n  parts {\n    ...AxiePart\n    __typename\n  }\n  stats {\n    ...AxieStats\n    __typename\n  }\n  auction {\n    ...AxieAuction\n    __typename\n  }\n  ownerProfile {\n    name\n    __typename\n  }\n  battleInfo {\n    ...AxieBattleInfo\n    __typename\n  }\n  children {\n    id\n    name\n    class\n    image\n    title\n    stage\n    __typename\n  }\n  __typename\n}\n\nfragment AxieBattleInfo on AxieBattleInfo {\n  banned\n  banUntil\n  level\n  __typename\n}\n\nfragment AxiePart on AxiePart {\n  id\n  name\n  class\n  type\n  specialGenes\n  stage\n  abilities {\n    ...AxieCardAbility\n    __typename\n  }\n  __typename\n}\n\nfragment AxieCardAbility on AxieCardAbility {\n  id\n  name\n  attack\n  defense\n  energy\n  description\n  backgroundUrl\n  effectIconUrl\n  __typename\n}\n\nfragment AxieStats on AxieStats {\n  hp\n  speed\n  skill\n  morale\n  __typename\n}\n\nfragment AxieAuction on Auction {\n  startingPrice\n  endingPrice\n  startingTimestamp\n  endingTimestamp\n  duration\n  timeLeft\n  currentPrice\n  currentPriceUSD\n  suggestedPrice\n  seller\n  listingIndex\n  state\n  __typename\n}\n"
  }

  aa = requests.post('https://graphql-gateway.axieinfinity.com/graphql', json=data)
  bb = aa.json()
  seller = bb['data']['axie']['auction']['seller']
  listing_inx = bb['data']['axie']['auction']['listingIndex']
  listing_stat = bb['data']['axie']['auction']['state']
  price = bb['data']['axie']['auction']['currentPrice']
  golden.append(seller)
  golden.append(listing_inx)
  golden.append(listing_stat)
  golden.append(price)
  return golden


def img_axie(axie_id):
    data = {
      "operation": "GetAxieDetail",
      "variables": {
        "axieId": "{}".format(axie_id)
      },
      "query": "query GetAxieDetail($axieId: ID!) {\n  axie(axieId: $axieId) {\n    ...AxieDetail\n    __typename\n  }\n}\n\nfragment AxieDetail on Axie {\n  id\n  image\n  class\n  chain\n  name\n  genes\n  owner\n  birthDate\n  bodyShape\n  class\n  sireId\n  sireClass\n  matronId\n  matronClass\n  stage\n  title\n  breedCount\n  level\n  figure {\n    atlas\n    model\n    image\n    __typename\n  }\n  parts {\n    ...AxiePart\n    __typename\n  }\n  stats {\n    ...AxieStats\n    __typename\n  }\n  auction {\n    ...AxieAuction\n    __typename\n  }\n  ownerProfile {\n    name\n    __typename\n  }\n  battleInfo {\n    ...AxieBattleInfo\n    __typename\n  }\n  children {\n    id\n    name\n    class\n    image\n    title\n    stage\n    __typename\n  }\n  __typename\n}\n\nfragment AxieBattleInfo on AxieBattleInfo {\n  banned\n  banUntil\n  level\n  __typename\n}\n\nfragment AxiePart on AxiePart {\n  id\n  name\n  class\n  type\n  specialGenes\n  stage\n  abilities {\n    ...AxieCardAbility\n    __typename\n  }\n  __typename\n}\n\nfragment AxieCardAbility on AxieCardAbility {\n  id\n  name\n  attack\n  defense\n  energy\n  description\n  backgroundUrl\n  effectIconUrl\n  __typename\n}\n\nfragment AxieStats on AxieStats {\n  hp\n  speed\n  skill\n  morale\n  __typename\n}\n\nfragment AxieAuction on Auction {\n  startingPrice\n  endingPrice\n  startingTimestamp\n  endingTimestamp\n  duration\n  timeLeft\n  currentPrice\n  currentPriceUSD\n  suggestedPrice\n  seller\n  listingIndex\n  state\n  __typename\n}\n"
    }

    a = requests.post('https://graphql-gateway.axieinfinity.com/graphql', json=data)
    a = a.json()
    return a['data']['axie']['image']

while(True):
    block_id = requests.get('https://api.covalenthq.com/v1/2020/block_v2/latest/?key=your_api_key')
    poar = block_id.json()
    block_id = int(poar['data']['items'][0]['height']) + 5


    try:
        for c in range(13, 0, -1):
            trymente = requests.get('https://ronin.rest/ronin/getBlock/{}'.format(block_id + c))
            if trymente.text != '{"error":"Block not found"}':
                sarapateu = c
                break

        # estava até 13
        for c in range(sarapateu, sarapateu + 5):
            print('block:', c)
            trymente = requests.get('https://ronin.rest/ronin/getBlock/{}'.format(block_id + c))
            if trymente.text != '{"error":"Block not found"}':
                content1 = trymente.json()
                content1 = content1['transactions']
                for c2 in content1:
                    trx_2 = requests.get('https://ronin.rest/ronin/decodeTransaction/{}'.format(c2))
                    content2 = trx_2.json()
                    try:
                        if content2['decodedInput']['name'] == 'createAuction':
                            content3 = content2['decodedInput']['params'][2]['value'][0]
                            link = content3
                            weth = int(content2['decodedInput']['params'][3]['value'][0]) / 1000000000000000000
                            preco =  int(content2['decodedInput']['params'][3]['value'][0]) / 1000000000000000000

                            if preco <= 0.0052 and len(str(preco)) < 8: # your price preference
                                print('axie encontrado: \nhttps://marketplace.axieinfinity.com/axie/{}\nvalue: {}'.format(link, preco))
                                eita = compra_axie(link)

                            # print(link)
                            # print('WETH:', preco)
                            print('https://marketplace.axieinfinity.com/axie/{}'.format(link))
                            print('WETH:', weth)
                            lista_axie = (link)
                            lista_price = (preco)
                            lista_img = (img_axie(content3))
                            print(lista_axie)
                            print(lista_price)
                            print(lista_img)
                        else:
                            pass
                    except:
                        pass

            else:
                pass
    except:
        print('esperando recarregar o uso da API')



