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

gl = NS(Contract=object, public=Public(), message=NS(sender_address='buyer'), message_raw={'datetime':datetime.fromtimestamp(1000,timezone.utc).isoformat()},
        vm=NS(UserError=UserError, Return=Return, run_nondet_unsafe=consensus),
        eq_principle=NS(strict_eq=lambda f:f()), nondet=NS(web=NS(get=get),exec_prompt=lambda *a,**k:dict(model) if type(model) is dict else model))
sys.modules['genlayer'] = types.ModuleType('genlayer'); sys.modules['genlayer'].gl=gl
spec=importlib.util.spec_from_file_location('contract','contracts/quote_parity.py'); module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

BUYER = '0x' + '1' * 40
SUPPLIER = '0x' + '2' * 40
OTHER = '0x' + '3' * 40

class ContractTests(unittest.TestCase):
    def setUp(self):
        gl.message.sender_address=BUYER; self.time(1000); web.clear()
        global model
        model = {}
        model.update(scope=['covered','covered'],prices_match=True)
        self.c=module.QuoteParity()
        self.c.create_request('Laptop supply',json.dumps(['Delivery included','24 month warranty']),10,'USD',1100,100,json.dumps([SUPPLIER,OTHER]))
        gl.message.sender_address=SUPPLIER
    def time(self,t): gl.message_raw['datetime']=datetime.fromtimestamp(t,timezone.utc).isoformat()
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
        self.bid('A',10000,3); gl.message.sender_address=OTHER; self.bid('B',9990,4)
        for i in range(2):self.c.evaluate_quote(0,i)
        self.time(1100);self.assertEqual(json.loads(self.c.finalize_request(0))['ranking'],[1,0])
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
        with self.assertRaises(UserError):self.c.create_request('X','["a"]',True,'USD',1100,0,json.dumps([SUPPLIER,OTHER]))
        with self.assertRaises(UserError):self.c.create_request('X','["a","a"]',1,'USD',1100,0,json.dumps([SUPPLIER,OTHER]))

    def test_uninvited_sybil_wallets_cannot_consume_slots(self):
        for i in range(25):
            gl.message.sender_address = '0x' + format(i + 100, '040x')
            with self.assertRaisesRegex(UserError, 'not invited'): self.bid('Sybil' + str(i))
        self.assertEqual(self.state()['bids'], [])
        gl.message.sender_address = SUPPLIER
        self.bid('Legitimate'); self.assertEqual(self.c.evaluate_quote(0,0), 'qualified')
    def test_one_invited_attacker_cannot_exhaust_another_slot(self):
        for i in range(3):
            self.bid('Bad' + str(i)); model['scope'] = ['excluded', 'covered']; self.c.evaluate_quote(0,i)
        with self.assertRaisesRegex(UserError, 'three bids'): self.bid('Fourth')
        gl.message.sender_address = OTHER
        model['scope'] = ['covered', 'covered']
        self.bid('Legitimate'); self.assertEqual(self.c.evaluate_quote(0,3), 'qualified')
        self.time(1100); self.assertEqual(json.loads(self.c.finalize_request(0))['ranking'], [3])
    def test_recovery_replaces_own_inconclusive_without_erasing_history(self):
        self.bid('Unclear'); model['scope'] = ['unclear', 'covered']; self.c.evaluate_quote(0,0)
        old = self.state()['bids'][0]['history']
        self.bid('Corrected'); model['scope'] = ['covered', 'covered']; self.c.evaluate_quote(0,1)
        self.assertEqual(self.state()['bids'][0]['history'], old)
        self.assertEqual(self.state()['bids'][0]['superseded_by'], 1)
        with self.assertRaisesRegex(UserError, 'superseded'): self.c.evaluate_quote(0,0)
        self.time(1100); self.assertEqual(json.loads(self.c.finalize_request(0))['ranking'], [1])
    def test_copying_document_cannot_steal_another_wallet_slot(self):
        self.bid('Copy')
        gl.message.sender_address = OTHER
        self.bid('Copy'); self.assertEqual(len(self.state()['active_bids']), 2)
        self.assertEqual(self.state()['bids'][1]['identity_status'], 'unverified_supplier_claim')
    def test_invalid_source_does_not_use_attempt(self):
        for _ in range(5):
            with self.assertRaises(UserError): self.c.submit_quote(0,'Bad','https://bad.example','a'*64,1,0,0,0,1)
        self.bid(); self.assertEqual(len(self.state()['bids']), 1)
    def test_malformed_json_is_structured_inconclusive(self):
        global model
        for raw in ['{broken', '```json {} ```', 'null', '[]', '"text"', '{"scope":["covered","covered"],"prices_match":1}', {'scope':['covered','covered'],'prices_match':True,'extra':1}]:
            self.setUp(); self.bid(); model = raw
            self.assertEqual(self.c.evaluate_quote(0,0), 'inconclusive')
            self.assertEqual(self.state()['bids'][0]['history'][0]['result']['source'], 'invalid_model_output')
    def test_distinct_qualifiers_and_exact_tie(self):
        self.bid('First',10000,3); self.c.evaluate_quote(0,0)
        gl.message.sender_address = OTHER
        self.bid('Second',10000,3); self.c.evaluate_quote(0,1)
        self.time(1100); self.assertEqual(json.loads(self.c.finalize_request(0))['ranking'], [0,1])
    def test_score_tie_prefers_landed_cost(self):
        self.bid('A',10000,3); self.c.evaluate_quote(0,0)
        gl.message.sender_address = OTHER
        self.bid('B',9990,4); self.c.evaluate_quote(0,1)
        self.time(1100); self.assertEqual(json.loads(self.c.finalize_request(0))['ranking'], [1,0])
    def test_superseded_qualified_offer_not_ranked(self):
        self.bid('Old'); self.c.evaluate_quote(0,0)
        self.bid('New'); model['scope'] = ['excluded','covered']; self.c.evaluate_quote(0,1)
        self.time(1100); self.assertEqual(json.loads(self.c.finalize_request(0))['ranking'], [])
    def test_model_and_web_exception_are_conservative(self):
        self.bid()
        original = gl.nondet.exec_prompt
        def fail(*a,**k): raise ValueError('provider failure')
        gl.nondet.exec_prompt = fail
        try:
            self.assertEqual(self.c.evaluate_quote(0,0),'inconclusive')
            self.assertEqual(self.state()['bids'][0]['history'][0]['result']['source'],'model_unavailable')
        finally: gl.nondet.exec_prompt = original
    def test_immutable_roster_validates_identity_and_bounds(self):
        gl.message.sender_address = BUYER
        for roster in ['not json', '[]', json.dumps([BUYER]),json.dumps([SUPPLIER,SUPPLIER]),json.dumps(['0x'+'0'*40]),json.dumps(['invalid']),json.dumps([SUPPLIER]*21)]:
            with self.assertRaises(UserError): self.c.create_request('X','["a"]',1,'USD',1100,0,roster)

    def test_full_invited_capacity_reserves_each_slot(self):
        gl.message.sender_address = BUYER
        wallets = ['0x' + format(i+50,'040x') for i in range(20)]
        c = module.QuoteParity(); c.create_request('Capacity','["Delivery","Warranty"]',1,'USD',1100,0,json.dumps(wallets))
        for i, sender in enumerate(wallets):
            gl.message.sender_address = sender
            for j in range(3):
                name = str(i) + '-' + str(j); body = name.encode(); url = 'https://quote.example/' + name
                web[url] = NS(status=200,body=body)
                c.submit_quote(0,name,url,sha256(body).hexdigest(),100,0,0,0,1)
        state = json.loads(c.get_request(0))
        self.assertEqual(len(state['bids']),60); self.assertEqual(len(state['active_bids']),20)
        self.assertEqual(sum(b['superseded_by'] is None for b in state['bids']),20)
    def test_failed_replacement_preserves_qualified_quote(self):
        self.bid(); self.c.evaluate_quote(0,0)
        with self.assertRaises(UserError): self.c.submit_quote(0,'Bad','https://bad.example','a'*64,1,0,0,0,1)
        self.assertIsNone(self.state()['bids'][0]['superseded_by'])
        self.time(1100); self.assertEqual(json.loads(self.c.finalize_request(0))['ranking'],[0])
    def test_large_model_output_is_inconclusive(self):
        global model
        self.bid(); model=' ' * 4001
        self.assertEqual(self.c.evaluate_quote(0,0),'inconclusive')
        self.assertEqual(self.state()['bids'][0]['history'][0]['result']['source'],'invalid_model_output')
    def test_unresolved_attacker_cannot_block_forever(self):
        self.bid('Attacker')
        gl.message.sender_address = OTHER; self.bid('Legitimate'); self.c.evaluate_quote(0,1)
        self.time(87501); self.assertEqual(json.loads(self.c.finalize_request(0))['ranking'],[1])

if __name__=='__main__':unittest.main()
