================================================================================
            Extract compilation commands from CMAKE
================================================================================

:Author: Scott Barclay

--------------------------------------------------------------------------------

First, let me say that the CMAKE environment that I am using may not match the
way other systems are configured. On my system, there are two source trees.

One of them is the normal tree: ``... SW/Source/Component/group/file.cpp``. The
other is a tree with the same structure: ``...
/SW/build/linux-debug/Source/Component/group``. However, the directories (such
as the "group" directory in the path) do not contain any source files. Instead,
this directory contains a directory called ``CMakeFiles``, a file called
``cmake_install.cmake`` and a file called ``Makefile`` (your mileage may vary).

Suppose the file you wish to clean is called **createTable.cpp**. First, you must
insure that the file has changed since the last build, since nothing will
happen if it is up to date. Also be sure that the directory has access to the
``cleanup.py`` file.

Next, descend to the directory containing the file::

    $ cd ... /SW/build/linux-debug/Source/Component/group

Then enter::

    $ make -n createTable.o

You will get a lot of output::

    .../SW/build/linux-debug/Source/Component/group$ make -n createTable.o
    cd ../../.. && make -f Source/Component/group/CMakeFiles/Group.dir/build.make
    Source/Component/group/CMakeFiles/Group.dir/createTable.cpp.o
    /usr/bin/cmake -E cmake_progress_report ../../../CMakeFiles /usr/bin/cmake -E cmake_echo_color --switch= --green
    "Building CXX object Source/Component/group/CMakeFiles/Group.dir/createTable.cpp.o"
    cd Source/Component/group && /remote/xtools/timesys/toolchain/bin/linux-gbueabi-g++
    -DARM_LINUX
    -DBOOST_NO_HASH -DBOOST_NO_NOEXCEPT -DBOOST_TR1_DISABLE_INCLUDE_NEXT -DCPU_ARM
    -DENABLE_ARM_DSP_BOOT=1 -DGPROF_BUILD -DKRING_DEBUG -DLINUX -DLINUXPEG -DLINUX_STUB -DLOGISSUE
    -DM_CONTEXT_IS_VOID -DNEDMALLOC_H -DNO_MEMBUF -DNVLOG_STRICT -DNVPLATFORM=2 -DNVTARGET_ENV
    -DNV_DEBUG_BUILD -DPLATFORM_G3PLUS -DSQLITE_SYSTEM_MALLOC -DUSE_NAMESPACES -DUSE_PFE_HW_MAP
    -DUSE_SYSLOG -D_ACE -D_DEBUG -std=c++11 -Wall -Wfatal-errors -Wno-non-template-friend -Wno-write-strings
    -Wno-reorder -Wno-sign-compare -Wno-unused-but-set-variable -Werror=unused-variable -Wno-format
    -Wno-unknown-pragmas --sysroot=/remote/xtools/timesys/toolchain -O0 -g2 -ggdb -funwind-tables -rdynamic
    -I../../../../../../Common -I../../../../../Source/Common -I../../../../../OTSS/ACE_6.1.5/arm/include
    -I../../../../../OTSS/boost_1_56_0 -I../../../../../OTSS/boost_1_56_0/boost -I../../../../../OTSS/trio-1.8
    -I../../../../../OTSS/libxml2/include -I../../../../../OTSS/libxslt -I../../../../../OTSS/libxslt/ZURTMAC/include/nucleus
    -I../../../../../OTSS/SQLite/include -I../../../../../OTSS/zlib121 -I../../../../../OTSS/zlib121/contrib/minizip
    -I../../../../../OTSS/zlib121/contrib/zurtmac -I../../../../../OTSS/NetBSD_2.1/libintl -I../../../../../OTSS/flexstring -
    .
    .
    (lots of include directories)
    .
    .
    I../../../../../Source/SystemServices/nvxmlparser -I../../../../../Source/FoundationClasses
    -I../../../../../Source/SystemComponents/DCMBase
    -Wno-deprecated -o CMakeFiles/Group.dir/createTable.cpp.o -c
    ../../../../../Source/Component/group/createTable.cpp

I have separated the first few commands, in real life they will appear one
right after another. (If the file has not changed, you will get two or three
lines which are not helpful). This last big chunk is the one I want. (I look
for the word "g++"). Since I am already in the ``Source/Component/group``
directory, I delete the first part, including the &&. Then I go to the end of
the chunk and find the words "Wno-deprecated". I take the phrase "-o
CMakeFiles/Group.dir/createTable.cpp.o" and move it to the end of the text.
Then remove the little "-c". (My compiler likes to see the name of the file to
be compiled, by itself without the "-c.")

The last part now looks like this::

    -Wno-deprecated ../../../../../Source/Components/group/createTable.cpp -o CMakeFiles/Group.dir/createTable.cpp.o

Now I copy the entire chunk into the clipboard. On the command line I type
"python cleanup.py " (note the trailing blank), then paste the chunk from the
clipboard at the cursor. Depending on what the final characters are, the
command may execute, or may wait for you to press the enter/return key.

At this point the program will begin analyzing the file::

    Checking compilation of ../../../../../Source/Component/group/createTable.cpp... OK
    Removing tableEncrypt.h (1/12)... not possible
    Removing NVEncrypt.h (2/12)... not possible
    Removing tableDatabase.h (3/12)... OK
    Removing openssl/conf.h (4/12)... OK
    Removing openssl/evp.h (5/12)... not possible
    Removing openssl/err.h (6/12)... not possible
    Removing openssl/rand.h (7/12)... not possible
    Removing openssl/sha.h (8/12)... not possible
    Removing string (9/12)... OK
    Removing NVFileSystem.h (10/12)... not possible
    Removing nvfstream.h (11/12)... not possible
    Removing NVStdio.h (12/12)... not possible
    ../../../../../Source/Component/group/createTable.cpp: not required tableDatabase.h, openssl/conf.h, string

In this case, three included files were not needed.
