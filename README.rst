================================================================================
                            Cleanup C++/C headers
================================================================================

This simple script helps in removing unnecessary includes from C/C++ files.

A huge code base or legacy code usually means that implementation files are
full of includes pilled up over years. Likewise, creating a new project by
forking an old one ends up with tons of leftovers.


How it works?
-----------------------------------------------------------

The only thing you need is **the full command** that creates an object file.

The script systematically comments out one include file at once and recompiles
source. When program/object file still compiles, then the commented out include
is considered unneeded.

**Caveat**, noticed by my colleague Leszek: such a mechanical way of removing
includes may lead to creating indirect dependencies. Some symbols required by
implementation might be provided (accidentally) by includes present in headers
files. When one remove include from the implementation file, then later changes
to the header file might break the compilation.


How to use it?
-----------------------------------------------------------

Here's an example from my toy project https://github.com/WojciechMula/avx512popcnt-superoptimizer

The head of the main program::

    $ head -n 15 avx512popcnt.cpp
    #include <cstdint>
    #include <cstdlib>
    #include <cstdio>
    #include <cassert>
    #include <vector>
    #include <memory>
    #include <random>
    #include <algorithm>
    #include <bitset>

    #include <sys/types.h>
    #include <unistd.h>

    #include "binary.cpp"

When run ``make``, we capture the command which builds the program::

    $ make avx512popcnt
    g++ -Wall -Wextra -pedantic -std=c++14 -O3 avx512popcnt.cpp -o lineavx512popcnt

Now the script comes::

    $ python cleanup.py g++ -Wall -Wextra -pedantic -std=c++14 -O3 avx512popcnt.cpp -o lineavx512popcnt
    Checking compilation... OK
    Removing cstdint... OK
    Removing cstdlib... OK
    Removing cstdio... OK
    Removing cassert... not possible
    Removing vector... OK
    Removing memory... not possible
    Removing random... not possible
    Removing algorithm... OK
    Removing bitset... OK
    Removing sys/types.h... OK
    Removing unistd.h... not possible
    Removing binary.cpp... not possible
    avx512popcnt.cpp: not required cstdint, cstdlib, cstdio, vector, algorithm, bitset, sys/types.h
    avx512popcnt.cpp was updated

It turned out that eight includes weren't needed at all.
