"""Deterministic contract harness. Uses SDK-shaped Response(status, body).
Not a replacement for live GenVM/validator tests documented in docs/live-run.json.
"""
import sys, types, unittest, json, importlib.util
from datetime import datetime, timezone
from hashlib import sha256
from types import SimpleNamespace as NS

class UserError(Exception): pass
class Return:
    def __init__(self, calldata): self.calldata = calldata
class Public:
    view = staticmethod(lambda f: f)
    write = staticmethod(lambda f: f)

model = {'scope':['covered','covered'], 'prices_match':True}
web = {}
def get(url):
    return web.get(url, NS(status=404, body=b''))
def consensus(leader, validator):
    result = leader()
    if not validator(Return(result)): raise UserError('consensus disagreement')
    return result

gl = NS(Contract=object, public=Public(), message=NS(sender_address='buyer', datetime=datetime.fromtimestamp(1000,timezone.utc)),
        vm=NS(UserError=UserError, Return=Return, run_nondet_unsafe=consensus),
        eq_principle=NS(strict_eq=lambda f:f()), nondet=NS(web=NS(get=get),exec_prompt=lambda *a,**k:dict(model)))
sys.modules['genlayer'] = types.ModuleType('genlayer'); sys.modules['genlayer'].gl=gl
spec=importlib.util.spec_from_file_location('contract','contracts/quote_parity.py'); module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

class ContractTests(unittest.TestCase):
    def setUp(self):
        gl.message.sender_address='buyer'; self.time(1000); web.clear()
        model.update(scope=['covered','covered'],prices_match=True)
        self.c=module.QuoteParity()
        self.c.create_request('Laptop supply',json.dumps(['Delivery included','24 month warranty']),10,'USD',1100,100)
    def time(self,t): gl.message.datetime=datetime.fromtimestamp(t,timezone.utc)
    def bid(self,name='Alpha',price=10000,days=3):
        body=f'Quote {name} {price}'.encode();url=f'https://quotes.example/{name}'
        web[url]=NS(status=200,body=body)
        return self.c.submit_quote(0,name,url,sha256(body).hexdigest(),price,0,0,0,days)
    def state(self): return json.loads(self.c.get_request(0))
    def test_create_submit_qualify_finalize(self):
        self.bid(); self.assertEqual(self.c.evaluate_quote(0,0),'qualified'); self.time(1100)
        result=json.loads(self.c.finalize_request(0));self.assertEqual(result['ranking'],[0])
        self.assertEqual(self.state()['bids'][0]['score'],100300)
    def test_reject_exclusions(self):
        self.bid(); model['scope']=['excluded','covered'];self.assertEqual(self.c.evaluate_quote(0,0),'rejected')
        self.time(1100);self.assertEqual(json.loads(self.c.finalize_request(0))['outcome'],'no_qualifying_bids')
    def test_reject_incorrect_structured_prices(self):
        self.bid();model['prices_match']=False;self.assertEqual(self.c.evaluate_quote(0,0),'rejected')
    def test_unclear_is_not_qualified(self):
        self.bid();model['scope']=['unclear','covered'];self.assertEqual(self.c.evaluate_quote(0,0),'inconclusive')
    def test_changed_document_not_proof(self):
        self.bid();web['https://quotes.example/Alpha'].body=b'changed';self.assertEqual(self.c.evaluate_quote(0,0),'inconclusive')
        self.assertEqual(self.state()['bids'][0]['history'][0]['result']['source'],'source_changed')
    def test_unavailable_document_on_submit(self):
        with self.assertRaisesRegex(UserError,'source_unavailable'):
            self.c.submit_quote(0,'X','https://bad.example','a'*64,1,0,0,0,2)
        self.assertEqual(self.state()['bids'],[])
    def test_unavailable_after_submit(self):
        self.bid();web.clear();self.assertEqual(self.c.evaluate_quote(0,0),'inconclusive')
    def test_wrong_hash_rejected(self):
        web['https://x.example']=NS(status=200,body=b'ok')
        with self.assertRaisesRegex(UserError,'incorrect hash'):
            self.c.submit_quote(0,'X','https://x.example','a'*64,1,0,0,0,2)
    def test_no_early_finalize_or_late_bid(self):
        with self.assertRaises(UserError):self.c.finalize_request(0)
        self.time(1100)
        with self.assertRaises(UserError):self.bid()
    def test_retry_cap_and_append_only_history(self):
        self.bid();model['scope']=['unclear','covered']
        for _ in range(3):self.c.evaluate_quote(0,0)
        self.assertEqual(len(self.state()['bids'][0]['history']),3)
        with self.assertRaises(UserError):self.c.evaluate_quote(0,0)
    def test_pending_blocks_finalization_until_timeout(self):
        self.bid();self.time(1100)
        with self.assertRaisesRegex(UserError,'unresolved'):self.c.finalize_request(0)
        self.time(87501);self.assertEqual(json.loads(self.c.finalize_request(0))['ranking'],[])
    def test_formula_and_tie_break(self):
        self.bid('A',10000,3);self.bid('B',9990,4);self.bid('C',9000,10)
        for i in range(3):self.c.evaluate_quote(0,i)
        self.time(1100);self.assertEqual(json.loads(self.c.finalize_request(0))['ranking'],[2,1,0])
    def test_duplicate_and_sender_limit(self):
        self.bid()
        with self.assertRaisesRegex(UserError,'duplicate'):self.bid()
        self.bid('B');self.bid('C')
        with self.assertRaisesRegex(UserError,'three bids'):self.bid('D')
    def test_no_mutation_after_close(self):
        self.bid();self.c.evaluate_quote(0,0);self.time(1100);self.c.finalize_request(0)
        with self.assertRaises(UserError):self.c.evaluate_quote(0,0)
        with self.assertRaises(UserError):self.c.finalize_request(0)
    def test_invalid_integer_and_requirements(self):
        with self.assertRaises(UserError):self.c.create_request('X','["a"]',True,'USD',1100,0)
        with self.assertRaises(UserError):self.c.create_request('X','["a","a"]',1,'USD',1100,0)

if __name__=='__main__':unittest.main()
