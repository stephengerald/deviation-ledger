from pathlib import Path
import json

CONTRACT = Path(__file__).resolve().parents[2] / "contracts" / "deviation_ledger.py"
SDK = "v0.2.16"
PROMPT = "Independently classify one change from a preregistered study plan"
TITLE = "Public park wayfinding comprehension study"
POLICY = "EXPECTED means expressly allowed by the frozen plan. JUSTIFIED requires a documented unforeseen constraint and a proportionate response. Otherwise classify UNEXPLAINED. Impact is high only when interpretation can materially change."


def deploy(vm, direct_deploy, alice, bob):
    vm.sender = alice
    return direct_deploy(str(CONTRACT), "0x" + bob.hex(), TITLE, POLICY, sdk_version=SDK)


def prepare(contract, vm, alice):
    contract.add_plan_section("sample", "Recruit forty adult volunteers at the east entrance and balance the two sign variants by alternating assignment.")
    contract.freeze_plan()


def test_record_classify_acknowledge_and_close(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_vm, direct_deploy, direct_alice, direct_bob)
    prepare(contract, direct_vm, direct_alice)
    direct_vm.sender = direct_bob
    contract.record_deviation("sample", "Recruitment moved to the west entrance for the final six volunteers.", "The east entrance was unexpectedly closed for emergency maintenance, so the same inclusion criteria were used at the west entrance.", "Recorded before those six volunteers were recruited.")
    direct_vm.mock_llm(PROMPT, json.dumps({"classification": "JUSTIFIED", "impact": "LOW"}))
    contract.classify_deviation(1)
    direct_vm.sender = direct_alice
    contract.acknowledge_deviation(1)
    contract.close_ledger()
    assert contract.get_state()["phase"] == "CLOSED"
    assert contract.get_deviation(1)["classification"] == "JUSTIFIED"
    leader = direct_vm._captured_validators[-1][0]
    assert direct_vm.run_validator(leader_result=leader) is True


def test_unexplained_entry_gets_one_answer_and_recheck(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_vm, direct_deploy, direct_alice, direct_bob)
    prepare(contract, direct_vm, direct_alice)
    direct_vm.sender = direct_bob
    contract.record_deviation("sample", "Removed twelve low-scoring responses after viewing the result distribution.", "The values looked unusual.", "Recorded after the primary comparison was calculated.")
    direct_vm.mock_llm(PROMPT, json.dumps({"classification": "UNEXPLAINED", "impact": "HIGH"}))
    contract.classify_deviation(1)
    contract.answer_unexplained(1, "The twelve records were exact duplicate device submissions identified by preexisting device hashes; the analysis was rerun with and without them.")
    direct_vm.clear_mocks()
    direct_vm.mock_llm(PROMPT, json.dumps({"classification": "JUSTIFIED", "impact": "MEDIUM"}))
    contract.classify_deviation(1)
    assert contract.get_deviation(1)["recheck_used"] is True
    with direct_vm.expect_revert("only_unexplained_can_be_answered"):
        contract.answer_unexplained(1, "A second answer must not be accepted after the one permitted response and completed recheck.")


def test_roles_and_model_output_fail_closed(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    contract = deploy(direct_vm, direct_deploy, direct_alice, direct_bob)
    direct_vm.sender = direct_charlie
    with direct_vm.expect_revert("only_principal"):
        contract.add_plan_section("sample", "An unrelated account must not be able to rewrite the preregistered plan section.")
    direct_vm.sender = direct_alice
    prepare(contract, direct_vm, direct_alice)
    direct_vm.sender = direct_bob
    contract.record_deviation("sample", "Moved one interview to the following morning.", "The participant requested the change before any interview began.", "Recorded before data collection.")
    direct_vm.mock_llm(PROMPT, json.dumps({"classification": "FINE", "impact": "LOW"}))
    with direct_vm.expect_revert("invalid_deviation_result"):
        contract.classify_deviation(1)
    assert contract.get_state()["classified_count"] == 0
