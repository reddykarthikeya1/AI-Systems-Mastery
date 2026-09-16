"""STARTER - Module 11: Networking Sockets HTTP

Multi-Client Asynchronous TCP Chat Server.

How to work
-----------
1. Read ../PROJECT_GUIDE.md and pick your tier (1 = guided, 3 = architect).
2. Fill in every `raise NotImplementedError` below, top to bottom. The
   signatures and docstrings are the specification - do not change them, or the
   shipped tests will not fit your code.
3. Grade yourself continuously:

       pytest ../project_solution/test_chat_server.py -v

   Point it at THIS file by running from `starter/`, or copy the test file next
   to your work. Red -> green is the whole loop.
4. Only after your tests pass, read ../project_solution/chat_server.py and compare.
   Reading the answer first costs you the entire exercise.

Every `# TODO:` line is a nudge, not a solution. The docstring above each
function is the real contract.
"""

from __future__ import annotations
import asyncio

class AsyncChatServer:
    """Multi-client broadcast TCP chat server."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8888) -> None:
        # [Tier 1] Algorithm: Initialize class instance attributes and validate
        #   baseline invariants.
        # HINTS:
        #  - Set default collections using factories to avoid shared mutable
        #   state.
        #  - Verify required parameters are non-None and within expected domain
        #   ranges.
        # GRADES: test_chat_server_connection_and_broadcast
        # WARNING: Avoid storing mutable defaults directly in class-level
        #   definitions.
        raise NotImplementedError("Module 11: implement AsyncChatServer.__init__()")


    async def broadcast(self, message: str, sender_id: str | None = None) -> None:
        """Sends a message to all connected clients except optionally the sender."""
        # [Tier 2] Algorithm: Implement AsyncChatServer.broadcast adhering to
        #   the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_chat_server_connection_and_broadcast
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 11: implement AsyncChatServer.broadcast()")


    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """Handles lifecycle and message loop for a single connected client."""
        # [Tier 2] Algorithm: Implement AsyncChatServer.handle_client adhering
        #   to the contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_client_quit_command
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 11: implement AsyncChatServer.handle_client()")


    async def start(self) -> None:
        """Starts listening for incoming connections."""
        # [Tier 2] Algorithm: Implement AsyncChatServer.start adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_server_stop_when_not_started
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 11: implement AsyncChatServer.start()")


    async def stop(self) -> None:
        """Closes all client connections and shuts down the server."""
        # [Tier 2] Algorithm: Implement AsyncChatServer.stop adhering to the
        #   contract defined in docstring.
        # HINTS:
        #  - Check preconditions on input arguments before mutating internal
        #   state.
        #  - Return expected data shape matching the type annotations.
        # GRADES: test_server_stop_when_not_started
        # WARNING: Do not alter the function signature or return incompatible
        #   types.
        raise NotImplementedError("Module 11: implement AsyncChatServer.stop()")



async def main() -> None:
    # [Tier 2] Algorithm: Entrypoint coordinator: parse CLI args, invoke
    #   workflow, exit with code.
    # HINTS:
    #  - Read arguments or configuration and instantiate primary pipeline
    #   engine.
    #  - Format output cleanly for console display and return exit code 0 on
    #   success.
    # GRADES: test_chat_server_connection_and_broadcast
    # WARNING: Return non-zero exit code if fatal execution errors occur.
    raise NotImplementedError("Module 11: implement main()")


if __name__ == "__main__":
    asyncio.run(main())
