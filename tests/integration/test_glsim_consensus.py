from __future__ import annotations
import json
from pathlib import Path
from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address

PROMPT = "Independently classify one change from a preregistered study plan"


def context():
    validators = get_validator_factory().batch_create_mock_validators(5, mock_llm_response={"nondet_exec_prompt": {PROMPT: json.dumps({"classification": "JUSTIFIED", "impact": "LOW"})}})
    return {"validators": [validator.to_dict() for validator in validators]}


def ok(receipt):
    assert tx_execution_succeeded(receipt)


def test_five_validator_deviation_lifecycle():
    principal, researcher = create_accounts(2)
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "deviation_ledger.py")
    args = [researcher.address, "Public park wayfinding comprehension study", "EXPECTED means allowed by the frozen plan. JUSTIFIED requires a documented unforeseen constraint and proportionate response. Otherwise UNEXPLAINED."]
    deployed = factory.deploy_contract_tx(args=args, account=principal, wait_transaction_status=TransactionStatus.FINALIZED)
    ok(deployed)
    address = extract_contract_address(deployed)
    principal_contract = factory.build_contract(address, account=principal)
    researcher_contract = factory.build_contract(address, account=researcher)
    ok(principal_contract.add_plan_section(args=["sample", "Recruit forty adult volunteers at the east entrance and alternate assignment between two sign variants."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(principal_contract.freeze_plan(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(researcher_contract.record_deviation(args=["sample", "Moved the final six recruitments to the west entrance.", "The east entrance was unexpectedly closed, so identical criteria were used at the west entrance.", "Recorded before those six volunteers were recruited."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(researcher_contract.classify_deviation(args=[1]).transact(transaction_context=context(), wait_transaction_status=TransactionStatus.FINALIZED))
    ok(principal_contract.acknowledge_deviation(args=[1]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(principal_contract.close_ledger(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    assert principal_contract.get_state(args=[]).call()["phase"] == "CLOSED"

