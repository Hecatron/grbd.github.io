#! python3
import os, sys, subprocess, shutil
import socketserver, threading
from pelican.server import ComplexHTTPRequestHandler

# Pelican Build Script
class PelicanBuild(object):

    # Class Init
    def __init__(self):
        self.BUILDDIR = "output"
        self.PELICANDIR = os.path.abspath("./")
        self.PORT = 8000
        self.github_pages_branch = "master"

    # Run a command
    def run_cmd(self, cmdarray, workingdir):
        proc = subprocess.Popen(cmdarray, cwd=workingdir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        proc_out, proc_err = proc.communicate()
        print(proc_out)
        print(proc_err)
        if proc.returncode != 0:
            raise RuntimeError("Failure to run command")
        return

    # Empty a Directory
    def emptydir(self, top):
        if(top == '/' or top == "\\"): return
        else:
            for root, dirs, files in os.walk(top, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))

    # Print Usage
    def usage(self):
        print ("Please use build.py <target> where <target> is one of")
        print ("  build         to make standalone HTML files")
        print ("  clean         to clean the output directory:" + self.BUILDDIR)
        print ("  publish       publish the site to the gh-pages branch")
        print ("  serve         Serve the site out on a port for demoing")

    # Build Pelican site using default config
    def build(self):
        self.clean()
        print("Building Pelican Site")
        cmdopts = ["C:\Python35\Scripts\pelican", "-s", "conf\pelicanconf.py", "-o", self.BUILDDIR]
        self.run_cmd(cmdopts, self.PELICANDIR)
        print ("Build finished. The HTML pages are in " + self.BUILDDIR)

    # Publish to GitHub Pages
    def publish(self):
        self.clean()
        print("Generating Html via pelican publish settings")
        cmdopts = ["C:\Python35\Scripts\pelican", "-s", "conf\publishconf.py", "-o", self.BUILDDIR]
        self.run_cmd(cmdopts, self.PELICANDIR)
        print("Running ghp-import")
        cmdopts = ["C:\Python35\Scripts\ghp-import.exe", "-b", self.github_pages_branch, self.BUILDDIR]
        self.run_cmd(cmdopts, self.PELICANDIR)
        print ("Pushing git repo: " + self.github_pages_branch)
        cmdopts = ["git", "push", "origin", self.github_pages_branch]
        self.run_cmd(cmdopts, self.PELICANDIR)
        print ("Site published to http://grbd.github.io")

    # Serve the files out for editing
    def serve(self):
        self.build()
        print("Starting MkDocs Server http://127.0.0.1:8000")
        os.chdir(self.BUILDDIR)
        class AddressReuseTCPServer(socketserver.TCPServer):
            allow_reuse_address = True
        server = AddressReuseTCPServer(('', self.PORT), ComplexHTTPRequestHandler)
        sys.stderr.write('Serving on port {0} ...\n'.format(self.PORT))
        t = threading.Thread(target=server.serve_forever)
        t.setDaemon(True) # don't hang on exit
        t.start()
        self.regenerate()
        print ("Server Closed.")

    # Automatically regenerate site upon file modification
    def regenerate(self):
        print ("Running in regenerate mode.")
        cmdopts = ["C:\Python35\Scripts\pelican", "-r", "-s", "conf\pelicanconf.py", "-o", self.BUILDDIR]
        self.run_cmd(cmdopts, self.PELICANDIR)

    # Clean the Build directory
    def clean(self):
        self.emptydir("output")
        print ("Clean finished")

    def main(self):
        if len(sys.argv) != 2:
            self.usage()
            return
        if sys.argv[1] == "build":
            self.build()
        if sys.argv[1] == "clean":
            self.clean()
        if sys.argv[1] == "publish":
            self.publish()
        if sys.argv[1] == "serve":
            self.serve()
        if sys.argv[1] == "regenerate":
            self.regenerate()

if __name__ == "__main__":
    PelicanBuild().main()