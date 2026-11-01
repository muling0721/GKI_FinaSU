#!/usr/bin/env python3
"""Add tcp_snd_cwnd accessors to kernels that predate their stable backport.

BBRv3 uses tcp_snd_cwnd()/tcp_snd_cwnd_set(); 5.15.41 and older 5.15
kernels do not provide them yet. The 5.10 BBRv3 patch already carries
the same helpers, so this is only needed for kernels where they are
missing.
"""

import pathlib
import sys

HEADER = pathlib.Path("include/net/tcp.h")
ANCHOR = "static inline bool tcp_in_slow_start(const struct tcp_sock *tp)\n"

HELPERS = (
    "static inline u32 tcp_snd_cwnd(const struct tcp_sock *tp)\n"
    "{\n"
    "\treturn tp->snd_cwnd;\n"
    "}\n"
    "\n"
    "static inline void tcp_snd_cwnd_set(struct tcp_sock *tp, u32 val)\n"
    "{\n"
    "\tWARN_ON_ONCE((int)val <= 0);\n"
    "\ttp->snd_cwnd = val;\n"
    "}\n"
    "\n"
)


def main() -> int:
    if not HEADER.is_file():
        print("include/net/tcp.h not found", file=sys.stderr)
        return 1

    text = HEADER.read_text(encoding="utf-8")
    if "tcp_snd_cwnd" in text:
        print("tcp_snd_cwnd helpers already present")
        return 0
    if ANCHOR not in text:
        print("anchor tcp_in_slow_start() not found in include/net/tcp.h", file=sys.stderr)
        return 1

    HEADER.write_text(text.replace(ANCHOR, HELPERS + ANCHOR, 1), encoding="utf-8")
    print("added tcp_snd_cwnd helpers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
