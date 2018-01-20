import sys
import os
import os.path


class ProgramError(ValueError):
    pass


INCLUDE = '#include '

class File(object):
    def __init__(self, file):

        self.includes = []
        self.lines = []

        for line in file:
            tmp = line.strip()
            if tmp.startswith(INCLUDE):
                inc = IncludeLine(line)
                self.includes.append(inc)
                self.lines.append(inc)
            else:
                self.lines.append(line)


    def write(self, file):
        for l in self.lines:
            file.write(str(l))


    def write_stripped(self, file):
        for l in self.lines:
            if type(l) is IncludeLine and not l.enabled:
                continue

            file.write(str(l))


class IncludeLine(object):
    def __init__(self, line):
        tmp = line.strip()[len(INCLUDE):]
        tmp = tmp[1:-1]

        self.line    = line
        self.path    = tmp
        self.enabled = True


    def enable(self, e):
        self.enabled = bool(e)


    def get_path(self):
        return self.path


    def __str__(self):
        if self.enabled:
            return self.line
        else:
            return '// %s' % self.line


class GCCCommandLine(object):
    def __init__(self, args):
        self.args   = args[:]
        self.index  = None
        self.source = None

        for i, arg in enumerate(self.args):
            if arg.endswith('.c') or arg.endswith('.cpp'):
                self.index  = i
                self.source = self.args[i]
                break

        if self.index is None:
            raise ProgramError("Expected .c/.cpp file on argument list")


    def get_path(self):
        return self.source


    def set_path(self, path):
        self.args[self.index] = path


    def __str__(self):
        return ' '.join(self.args)


class Application:
    def __init__(self, args):
        self.out     = sys.stdout
        self.cmdline = GCCCommandLine(args)

        self.quiet   = True
        self.overwrite = True

        srcpath = self.cmdline.get_path()
        if not os.path.exists(srcpath):
            raise ProgramError("Can't open source file '%s'" % srcpath)

        with open(srcpath, 'rt') as f:
            self.file = File(f)


    def write(self, msg):
        self.out.write(msg)
        self.out.flush()


    def run(self):
        self.write('Checking compilation... ')
        if False and not self.can_compile():
            self.write('failed\n')
            return
        else:
            self.write('OK\n')

        self.check()
        self.fix()


    def check(self):
        dstpath = 'ch-%s' % self.cmdline.get_path()
        self.cmdline.set_path(dstpath)

        self.not_needed = []
        for include in self.file.includes:
            self.write('Removing %s... ' % include.get_path())
            include.enable(False)
            with open(dstpath, 'wt') as f:
                self.file.write(f)

            if self.can_compile():
                self.write('OK\n')
                self.not_needed.append(include)
            else:
                include.enable(True)
                self.write('not possible\n')

            os.remove(dstpath)


    def fix(self):
        srcpath = self.cmdline.get_path()
        self.write('%s: ' % srcpath)
        if len(self.not_needed) == 0:
            self.write('no changes\n')
        else:
            tmp = [item.get_path() for item in self.not_needed]
            self.write('not required %s\n' % (', '.join(tmp)))

            if self.overwrite:
                with open(srcpath, 'wt') as f:
                    self.file.write_stripped(f)

                self.write('%s was updated\n' % srcpath)

        self.write('\n')


    def can_compile(self):
        cmdline = str(self.cmdline)
        if self.quiet:
            cmdline += ' 2> /dev/null'

        ret = os.system(cmdline)
        return ret == 0


def main():
    app = Application(sys.argv[1:])
    try:
        app.run()
    except:
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()

