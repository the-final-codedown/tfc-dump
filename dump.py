import datetime
import falcon
import requests


class DumpInfo:
    account_url = None
    profile_url = None


def getTransactions(transactions, accountId):
    if not transactions:
        return []
    for transaction in transactions:
        if '.' not in transaction["date"]:
            transaction["date"] = transaction["date"] + '.0'
    print(accountId)
    print(transactions)
    transactionsFiltered = []
    transactions.sort(key=lambda r: datetime.datetime.strptime(r["date"], '%Y-%m-%dT%H:%M:%S.%f'), reverse=True)
    print(transactions)
    i = 0
    for transaction in transactions:
        if i >= 10: break
        if transaction['source'] == accountId or transaction['receiver'] == accountId:
            i = i + 1
            transactionsFiltered.append(transaction)
    return transactionsFiltered


def getAccounts(accounts, email):
    accountsFiltered = []
    for account in accounts:
        if account['owner']['email'] == email:
            accountsFiltered.append(account)
    return accountsFiltered


# port : 8083
class DumpController(object):
    def on_get(self, req, resp):
        result = ''
        savingsAccount = requests.get(DumpInfo.account_url + '/accounts/SAVINGS/' + 'accounts')
        print(savingsAccount.json())
        checksAccount = requests.get(DumpInfo.account_url + '/accounts/CHECK/' + 'accounts')
        print(checksAccount.json())
        transactions = requests.get(DumpInfo.account_url + '/transactions')
        profiles = requests.get(DumpInfo.profile_url + '/profiles')
        for profile in profiles.json():
            print(profile)
            accountsFiltered = getAccounts(savingsAccount.json(), profile['_id']) + getAccounts(checksAccount.json(),
                                                                                                profile['_id'])
            result += profile['_id'] + '   ' + str(len(accountsFiltered)) + ' Accounts\n'
            for account in accountsFiltered:
                result += ' account : ' + account['accountId'] + '\n'
                transactionsFiltered = getTransactions(transactions.json(), account['accountId'])
                result += '   Money : ' + str(account['money']) + '   transaction : ' + str(
                    len(transactionsFiltered)) + '\n\n'
                for transaction in transactionsFiltered:
                    result += '     transaction : '
                    if transaction['source'] == account['accountId']:
                        result += transaction['receiver'] + ' - ' + str(transaction['amount']) + '\n'
                    elif transaction['receiver'] == account['accountId']:
                        result += transaction['source'] + ' + ' + str(transaction['amount']) + '\n'
                result += '\n'
        resp.body = result
        resp.status = falcon.HTTP_200
        return resp


def setup_dump(account_url, profile_url):
    if account_url is not None and profile_url is not None:
        DumpInfo.account_url = account_url
        DumpInfo.profile_url = profile_url
        print(DumpInfo.account_url)
        print(DumpInfo.profile_url)
    app = falcon.API()

    dump_controller = DumpController()
    app.add_route('/dump', dump_controller)

    return app
