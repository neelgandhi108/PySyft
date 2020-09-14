# third party
import torch as th

# syft absolute
import syft as sy
from syft.core.common.uid import UID
from syft.core.node.common.action.function_or_constructor_action import (
    RunFunctionOrConstructorAction,
)

# TODO test execution
# TODO test permissions


def test_run_function_or_constructor_action_serde() -> None:
    alice = sy.VirtualMachine(name="alice")
    alice_client = alice.get_client()

    path = "torch.Tensor.add"
    args = (
        th.tensor([1, 2, 3]).send(alice_client),
        th.tensor([4, 5, 5]).send(alice_client),
    )
    kwargs = {}  # type: ignore
    id_at_location = UID()
    msg_id = UID()

    msg = RunFunctionOrConstructorAction(
        path=path,
        args=args,
        kwargs=kwargs,
        id_at_location=id_at_location,
        address=alice_client.address,
        msg_id=msg_id,
    )

    blob = msg.serialize()

    msg2 = sy.deserialize(blob=blob)

    assert msg2.path == msg.path
    # FIXME this cannot be checked before we fix the Pointer serde problem (see _proto2object in Pointer)
    # assert msg2.args == msg.args
    assert msg2.kwargs == msg.kwargs
    assert msg2.address == msg.address
    assert msg2.id == msg.id
    assert msg2.id_at_location == msg.id_at_location
