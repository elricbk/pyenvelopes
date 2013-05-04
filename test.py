from ExpenseManager import ExpenseManager
from EnvelopeManager import EnvelopeManager


try:
    envMgr = EnvelopeManager()
    expMgr = ExpenseManager()
    envMgr.setExpenseManager(expMgr)
    expMgr.setEnvelopeManager(envMgr)
    envMgr.printEnvelopes()
except Exception as e:
    print e

while 1:
    curLine = raw_input().strip()
    if curLine.startswith('env:'):
        try:
            env = curLine.split()[1]
            print('Envelope value for {0} = {1}'.format(env, envMgr.envelopeValue(envMgr.idForEnvName(env))))
            continue
        except Exception as e:
            print(e)

    if curLine.startswith('exp'):
        for ex in expMgr.expenses:
            print(ex)
        continue

    try:
        ex = expMgr.addExpense(curLine)
        print(ex)
        envMgr.printEnvelopes()
    except Exception as e:
        print(e)
    print('\n')





